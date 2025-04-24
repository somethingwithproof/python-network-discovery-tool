        ]

        manager = DeviceManager.from_dict(dict_list)
        assert len(manager) == 2

        device1 = manager.get_device(1)
        assert device1 is not None
        assert device1.id == 1
        assert device1.host == "example1.com"
        assert device1.ip == "192.168.1.1"
        assert device1.alive
        assert device1.snmp
        assert not device1.ssh
        assert device1.mysql
        assert device1.scanned

        device2 = manager.get_device(2)
        assert device2 is not None
        assert device2.id == 2
        assert device2.host == "example2.com"
        assert device2.ip == "192.168.1.2"
        assert not device2.alive
        assert not device2.snmp
        assert not device2.ssh
        assert not device2.mysql
        assert device2.errors == ["Error"]
        assert device2.scanned