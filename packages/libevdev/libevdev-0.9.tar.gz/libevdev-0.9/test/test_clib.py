import os
import unittest
import ctypes
from libevdev._clib import Libevdev, UinputDevice
from pathlib import Path

# Note: these tests test for the correct functioning of the python bindings,
# not of libevdev underneath. Some ranges are hardcoded for simplicity, e.g.
# if properties 1-4 work the others will work too if libevdev works
# correctly


def is_root():
    return os.getuid() == 0


def has_event_devices():
    return list(Path('/dev/input/').glob('event*'))


class TestNameConversion(unittest.TestCase):

    def test_type_max(self):
        for t in ["REL", "ABS"]:
            c = Libevdev.event_to_value("EV_{}".format(t), "{}_MAX".format(t))
            max = Libevdev.type_max("EV_{}".format(t))
            self.assertEqual(c, max)

    def test_prop_name(self):
        name = Libevdev.property_to_name(0)
        self.assertEqual(name, "INPUT_PROP_POINTER")

        prevname = None
        for i in range(5):
            name = Libevdev.property_to_name(i)
            self.assertIsNotNone(name)
            self.assertTrue(name.startswith("INPUT_PROP_"))
            self.assertNotEqual(prevname, name)
            prevname = name

    def test_prop_to_name_invalid(self):
        name = Libevdev.property_to_name(-1)
        self.assertIsNone(name)
        name = Libevdev.property_to_name(100)
        self.assertIsNone(name)
        with self.assertRaises(ctypes.ArgumentError):
            name = Libevdev.property_to_name("foo")

    def test_prop_to_value(self):
        value = Libevdev.property_to_value("INPUT_PROP_POINTER")
        self.assertEqual(value, 0)

        value = Libevdev.property_to_value("INPUT_PROP_DIRECT")
        self.assertEqual(value, 1)

    def test_prop_to_value_invalid(self):
        name = Libevdev.property_to_value("foo")
        self.assertIsNone(name)

    def test_type_to_name(self):
        name = Libevdev.event_to_name(1)
        self.assertEqual(name, "EV_KEY")

        prevname = None
        for i in range(5):
            name = Libevdev.event_to_name(i)
            self.assertIsNotNone(name)
            self.assertTrue(name.startswith("EV_"))
            self.assertNotEqual(prevname, name)
            prevname = name

    def test_type_to_name_invalid(self):
        name = Libevdev.event_to_name(-1)
        self.assertIsNone(name)
        name = Libevdev.event_to_name(100)
        self.assertIsNone(name)
        with self.assertRaises(ctypes.ArgumentError):
            name = Libevdev.event_to_name("foo")

    def test_code_to_name(self):
        name = Libevdev.event_to_name(0, 0)
        self.assertEqual(name, "SYN_REPORT")

        name = Libevdev.event_to_name(1, 1)
        self.assertEqual(name, "KEY_ESC")

    def test_code_to_name_invalid(self):
        name = Libevdev.event_to_name(0, 1000)
        self.assertIsNone(name)
        name = Libevdev.event_to_name(0, -1)
        self.assertIsNone(name)
        with self.assertRaises(ctypes.ArgumentError):
            name = Libevdev.event_to_name(0, "foo")

    def test_value_to_name(self):
        name = Libevdev.event_to_name(3, 0x37, 0)
        self.assertEqual(name, "MT_TOOL_FINGER")

        name = Libevdev.event_to_name(3, 0x37, 1)
        self.assertEqual(name, "MT_TOOL_PEN")

    def test_value_to_name_invalid(self):
        name = Libevdev.event_to_name(3, 0x37, 1000)
        self.assertIsNone(name)
        name = Libevdev.event_to_name(3, 0x37, -1)
        self.assertIsNone(name)
        with self.assertRaises(ctypes.ArgumentError):
            name = Libevdev.event_to_name(0, "foo")

    def test_event_type_to_value(self):
        v = Libevdev.event_to_value("EV_REL")
        self.assertEqual(v, 2)

    def test_event_type_to_value_invalid(self):
        v = Libevdev.event_to_value("foo")
        self.assertIsNone(v)
        with self.assertRaises(AttributeError):
            v = Libevdev.event_to_value(0)

    def test_event_code_to_value(self):
        v = Libevdev.event_to_value("EV_REL", "REL_Y")
        self.assertEqual(v, 1)

        v = Libevdev.event_to_value(0, "SYN_DROPPED")
        self.assertEqual(v, 3)

    def test_event_code_to_value_invalid(self):
        v = Libevdev.event_to_value("EV_REL", "KEY_ESC")
        self.assertIsNone(v)

    def test_event_value_to_value(self):
        v = Libevdev.event_to_value("EV_ABS", "ABS_MT_TOOL_TYPE", "MT_TOOL_FINGER")
        self.assertEqual(v, 0)

        v = Libevdev.event_to_value("EV_ABS", "ABS_MT_TOOL_TYPE", "MT_TOOL_PEN")
        self.assertEqual(v, 1)

    def test_event_value_to_value_invalid(self):
        v = Libevdev.event_to_value("EV_ABS", "ABS_X", "foo")
        self.assertIsNone(v)


class TestLibevdevDevice(unittest.TestCase):

    def test_ctx_init(self):
        dev = Libevdev()
        del dev

    def test_set_get_name(self):
        dev = Libevdev()
        name = dev.name
        self.assertEqual(name, '')

        dev.name = "foo"
        name = dev.name
        self.assertEqual(name, "foo")

        dev.name = None
        name = dev.name
        self.assertEqual(name, "")

    def test_set_get_uniq(self):
        dev = Libevdev()
        uniq = dev.uniq
        self.assertIsNone(uniq)

        dev.uniq = "foo"
        uniq = dev.uniq
        self.assertEqual(uniq, "foo")

        # libevdev issue: phys may be NULL (unlike the name) but we can't
        # set it to NULL. But the conversion code returns None for the empty
        # string, so let's test for that
        dev.uniq = None
        uniq = dev.uniq
        self.assertEqual(uniq, None)

    def test_set_get_phys(self):
        dev = Libevdev()
        phys = dev.phys
        self.assertIsNone(phys)

        dev.phys = "foo"
        phys = dev.phys
        self.assertEqual(phys, "foo")

        # libevdev issue: phys may be NULL (unlike the name) but we can't
        # set it to NULL. But the conversion code returns None for the empty
        # string, so let's test for that
        dev.phys = None
        phys = dev.phys
        self.assertEqual(phys, None)

    def test_get_driver_version(self):
        dev = Libevdev()
        v = dev.driver_version
        self.assertEqual(v, 0)
        # we can't set this, nothing else we can test

    def test_set_get_id(self):
        dev = Libevdev()
        id = dev.id
        self.assertEqual(id["bustype"], 0)
        self.assertEqual(id["vendor"], 0)
        self.assertEqual(id["product"], 0)
        self.assertEqual(id["version"], 0)

        id["bustype"] = 1
        id["vendor"] = 2
        id["product"] = 3
        id["version"] = 4

        dev.id = id
        id = dev.id
        self.assertEqual(id["bustype"], 1)
        self.assertEqual(id["vendor"], 2)
        self.assertEqual(id["product"], 3)
        self.assertEqual(id["version"], 4)

        del id["bustype"]
        del id["vendor"]
        del id["product"]
        id["version"] = 5

        dev.id = id
        id = dev.id
        self.assertEqual(id["bustype"], 1)
        self.assertEqual(id["vendor"], 2)
        self.assertEqual(id["product"], 3)
        self.assertEqual(id["version"], 5)


@unittest.skipUnless(has_event_devices(), 'Local event devices required')
class TestRealDevice(unittest.TestCase):
    """
    Tests various things against /dev/input/event3 which is usually the
    keyboard. Requires root rights though.
    """

    def setUp(self):
        self.fd = open("/dev/input/event3", "rb")

    def tearDown(self):
        self.fd.close()

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_fd(self):
        dev = Libevdev()
        dev.fd = self.fd
        fd = dev.fd
        self.assertEqual(self.fd, fd)

        fd2 = open("/dev/input/event3", "rb")
        dev.fd = fd2
        fd = dev.fd
        self.assertEqual(fd, fd2)
        fd2.close()

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_init_fd(self):
        dev = Libevdev(self.fd)
        fd = dev.fd
        self.assertEqual(self.fd, fd)

        fd2 = open("/dev/input/event3", "rb")
        dev.fd = fd2
        fd = dev.fd
        self.assertEqual(fd, fd2)
        fd2.close()

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_ids(self):
        dev = Libevdev(self.fd)
        id = dev.id
        self.assertNotEqual(id["bustype"], 0)
        self.assertNotEqual(id["vendor"], 0)
        self.assertNotEqual(id["product"], 0)
        self.assertNotEqual(id["version"], 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_name(self):
        dev = Libevdev(self.fd)
        name = dev.name
        self.assertNotEqual(name, "")

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_driver_version(self):
        dev = Libevdev(self.fd)
        v = dev.driver_version
        self.assertEqual(v, 0x010001)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_clock_id(self):
        dev = Libevdev(self.fd)
        try:
            import time
            clock = time.CLOCK_MONOTONIC
        except AttributeError:
            clock = 1
        rc = dev.set_clock_id(clock)
        self.assertEqual(rc, 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_grab(self):
        dev = Libevdev(self.fd)
        # no exception == success
        dev.grab()
        dev.grab(False)
        dev.grab(True)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_has_event(self):
        dev = Libevdev(self.fd)
        self.assertTrue(dev.has_event("EV_SYN", "SYN_REPORT"))

        type_supported = -1
        max_code = -1
        for t in range(1, 5):
            if dev.has_event(t):
                type_supported = t
                max_code = Libevdev.type_max(t)
                if max is None:
                    continue
                break

        self.assertGreater(type_supported, 0)

        codes_supported = 0
        for c in range(max_code + 1):
            if dev.has_event(type_supported, c):
                codes_supported += 1

        self.assertGreater(codes_supported, 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_has_property(self):
        """
        Let's assume at least one between event0 and event10 is a device
        with at least one property set. May cause false negatives.
        """

        props_supported = 0
        for i in range(10):
            try:
                with open("/dev/input/event{}".format(i), "rb") as fd:
                    dev = Libevdev(fd)

                    for p in range(6):
                        if dev.has_property(p):
                            props_supported += 1
            except IOError:
                # Not all eventX nodes are guaranteed to exist
                pass
        self.assertGreater(props_supported, 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_num_slots(self):
        """
        Let's assume that our device doesn't have slots
        """
        dev = Libevdev(self.fd)
        self.assertIsNone(dev.num_slots)


class TestAbsDevice(unittest.TestCase):
    """
    Tests various things against the first device with EV_ABS.
    We're relying on that this device has ABS_Y, this tests against a code
    that's nonzero and is the most common ABS anyway.
    Requires root rights.
    """

    def setUp(self):
        want_fd = None
        for i in range(20):
            try:
                fd = open("/dev/input/event{}".format(i), "rb")
                dev = Libevdev(fd)
                if dev.has_event("EV_ABS", "ABS_Y"):
                    want_fd = fd
                    break
                fd.close()
            except IOError:
                # Not all eventX nodes are guaranteed to exist
                pass

        if want_fd is None:
            self.skipTest('No abs device available')

        self.fd = want_fd

    def tearDown(self):
        self.fd.close()

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_absinfo(self):
        dev = Libevdev(self.fd)
        a = dev.absinfo("ABS_Y")
        self.assertTrue("minimum" in a)
        self.assertTrue("maximum" in a)
        self.assertTrue("resolution" in a)
        self.assertTrue("fuzz" in a)
        self.assertTrue("flat" in a)
        self.assertTrue("value" in a)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_absinfo(self):
        dev = Libevdev(self.fd)
        real_a = dev.absinfo("ABS_Y")
        a = dev.absinfo("ABS_Y")
        a["minimum"] = 100
        a["maximum"] = 200
        a["fuzz"] = 300
        a["flat"] = 400
        a["resolution"] = 500
        a["value"] = 600

        a = dev.absinfo("ABS_Y", new_values=a)
        self.assertEqual(a["minimum"], 100)
        self.assertEqual(a["maximum"], 200)
        self.assertEqual(a["fuzz"], 300)
        self.assertEqual(a["flat"], 400)
        self.assertEqual(a["resolution"], 500)
        self.assertEqual(a["value"], 600)

        l2 = Libevdev(self.fd)
        a2 = l2.absinfo("ABS_Y")
        self.assertNotEqual(a["minimum"], real_a["minimum"])
        self.assertNotEqual(a["maximum"], real_a["maximum"])
        self.assertNotEqual(a["fuzz"], real_a["fuzz"])
        self.assertNotEqual(a["flat"], real_a["flat"])
        self.assertNotEqual(a["resolution"], real_a["resolution"])
        self.assertEqual(a2["value"], real_a["value"])
        self.assertEqual(a2["minimum"], real_a["minimum"])
        self.assertEqual(a2["maximum"], real_a["maximum"])
        self.assertEqual(a2["fuzz"], real_a["fuzz"])
        self.assertEqual(a2["flat"], real_a["flat"])
        self.assertEqual(a2["resolution"], real_a["resolution"])
        self.assertEqual(a2["value"], real_a["value"])

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_absinfo_invalid(self):
        dev = Libevdev(self.fd)
        with self.assertRaises(ValueError):
            dev.absinfo("REL_X")

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_absinfo_kernel(self):
        # FIXME: yeah, nah, not testing that on a random device...
        pass

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_get_set_event_value(self):
        dev = Libevdev(self.fd)
        v = dev.event_value("EV_ABS", "ABS_Y")
        self.assertIsNotNone(v)
        v = dev.event_value(0x03, 0x01, new_value=300)
        self.assertEqual(v, 300)
        v = dev.event_value(0x03, 0x01)
        self.assertEqual(v, 300)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_get_set_event_value_invalid(self):
        dev = Libevdev(self.fd)
        v = dev.event_value("EV_ABS", 0x600)
        self.assertIsNone(v)
        v = dev.event_value(0x03, 0x600, new_value=300)
        self.assertIsNone(v)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_enable_event_code(self):
        dev = Libevdev(self.fd)

        self.assertFalse(dev.has_event("EV_REL", "REL_RY"))
        dev.enable("EV_REL", "REL_RY")
        self.assertTrue(dev.has_event("EV_REL", "REL_RY"))
        dev.disable("EV_REL", "REL_RY")
        self.assertFalse(dev.has_event("EV_REL", "REL_RY"))

        data = {"minimum": 100,
                "maximum": 200,
                "value": 300,
                "fuzz": 400,
                "flat": 500,
                "resolution": 600}
        self.assertFalse(dev.has_event("EV_ABS", "ABS_RY"))
        dev.enable("EV_ABS", "ABS_RY", data)
        self.assertTrue(dev.has_event("EV_ABS", "ABS_RY"))
        dev.disable("EV_ABS", "ABS_RY")
        self.assertFalse(dev.has_event("EV_ABS", "ABS_RY"))

        data = 1
        self.assertFalse(dev.has_event("EV_REP", "REP_DELAY"))
        dev.enable("EV_REP", "REP_DELAY", data)
        self.assertTrue(dev.has_event("EV_REP", "REP_DELAY"))
        dev.disable("EV_REP", "REP_DELAY")
        self.assertFalse(dev.has_event("EV_REP", "REP_DELAY"))

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_enable_property(self):
        dev = Libevdev(self.fd)
        self.assertFalse(dev.has_property("INPUT_PROP_ACCELEROMETER"))
        dev.enable_property("INPUT_PROP_ACCELEROMETER")
        self.assertTrue(dev.has_property("INPUT_PROP_ACCELEROMETER"))


@unittest.skipUnless(has_event_devices(), 'Local event devices required')
class TestMTDevice(unittest.TestCase):
    """
    Tests various things against the first MT device found.
    Requires root rights.
    """

    def setUp(self):
        want_fd = None
        for i in range(20):
            try:
                fd = open("/dev/input/event{}".format(i), "rb")
                dev = Libevdev(fd)
                if dev.num_slots is not None:
                    want_fd = fd
                    break
                fd.close()
            except IOError:
                # Not all eventX nodes are guaranteed to exist
                pass

        if want_fd is None:
            self.skipTest('No MT device available')
        self.fd = want_fd

    def tearDown(self):
        self.fd.close()

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_num_slots(self):
        dev = Libevdev(self.fd)
        self.assertGreater(dev.num_slots, 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_current_slot(self):
        dev = Libevdev(self.fd)
        self.assertGreaterEqual(dev.current_slot, 0)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_slot_value(self):

        dev = Libevdev(self.fd)
        a = dev.absinfo("ABS_MT_POSITION_X")
        v = dev.slot_value(dev.current_slot, "ABS_MT_POSITION_X")
        self.assertLessEqual(a["minimum"], v)
        self.assertGreaterEqual(a["maximum"], v)

    @unittest.skipUnless(is_root(), 'Test requires root')
    def test_set_slot_value(self):
        dev = Libevdev(self.fd)
        v = dev.slot_value(dev.current_slot, "ABS_MT_POSITION_X")
        v += 10
        v2 = dev.slot_value(dev.current_slot, "ABS_MT_POSITION_X", v)
        self.assertEqual(v, v2)
        v2 = dev.slot_value(dev.current_slot, "ABS_MT_POSITION_X")
        self.assertEqual(v, v2)


class TestUinput(unittest.TestCase):
    """
    Tests uinput device creation.
    Requires root rights.
    """

    def is_identical(self, d1, d2):
        for t in range(Libevdev.event_to_value("EV_MAX")):
            max = Libevdev.type_max(t)
            if max is None:
                continue
            for c in range(max):
                if d1.has_event(t, c) != d1.has_event(t, c):
                    return False
        return True

    @unittest.skipUnless(is_root(), 'Test requires root')
    def testRelative(self):
        dev = Libevdev()
        dev.name = "test device"
        dev.enable("EV_REL", "REL_X")
        dev.enable("EV_REL", "REL_Y")
        uinput = UinputDevice(dev)
        self.assertIsNotNone(uinput.devnode)

        with open(uinput.devnode) as f:
            newdev = Libevdev(f)
            self.assertTrue(self.is_identical(dev, newdev))

    @unittest.skipUnless(is_root(), 'Test requires root')
    def testButton(self):
        dev = Libevdev()
        dev.name = "test device"
        dev.enable("EV_KEY", "BTN_LEFT")
        dev.enable("EV_KEY", "KEY_A")
        uinput = UinputDevice(dev)
        self.assertIsNotNone(uinput.devnode)

        with open(uinput.devnode) as f:
            newdev = Libevdev(f)
            self.assertTrue(self.is_identical(dev, newdev))

    @unittest.skipUnless(is_root(), 'Test requires root')
    def testAbsolute(self):
        absinfo = {"minimum": 0,
                   "maximum": 1}

        dev = Libevdev()
        dev.name = "test device"
        dev.enable("EV_ABS", "ABS_X", absinfo)
        dev.enable("EV_ABS", "ABS_Y", absinfo)
        uinput = UinputDevice(dev)
        self.assertIsNotNone(uinput.devnode)

        with open(uinput.devnode) as f:
            newdev = Libevdev(f)
            self.assertTrue(self.is_identical(dev, newdev))

    @unittest.skipUnless(is_root(), 'Test requires root')
    def testDeviceNode(self):
        dev = Libevdev()
        dev.name = "test device"
        dev.enable("EV_REL", "REL_X")
        dev.enable("EV_REL", "REL_Y")
        uinput = UinputDevice(dev)
        self.assertTrue(uinput.devnode.startswith("/dev/input/event"))

    @unittest.skipUnless(is_root(), 'Test requires root')
    def testSyspath(self):
        dev = Libevdev()
        dev.name = "test device"
        dev.enable("EV_REL", "REL_X")
        dev.enable("EV_REL", "REL_Y")
        uinput = UinputDevice(dev)
        self.assertTrue(uinput.syspath.startswith("/sys/devices/virtual/input/input"))


if __name__ == '__main__':
    unittest.main()
