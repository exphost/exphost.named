def test_named_process(host):
    assert host.service("named").is_running
    assert host.service("named").is_enabled
def test_groups_mapping_responses(host):
    host.ansible(
        "command",
        "yum install -y bind-utils",
    become=True,
    check=False,
    )

    assert host.check_output("dig @127.0.0.1 test.some.example.domain.xyz +short")
    assert host.check_output("dig @127.0.0.1 role1.some.example.domain.xyz +short")
    assert host.check_output("dig @127.0.0.1 role2.some.example.domain.xyz +short")
    assert not host.check_output("dig @127.0.0.1 test2.some.example.domain.xyz +short")

def test_records_responses(host):
    host.ansible(
        "command",
        "yum install -y bind-utils",
    become=True,
    check=False,
    )

    assert host.check_output("dig @127.0.0.1 rec1.next.example.domain.xyz +short") == "1.2.3.4"
    assert host.check_output("dig @127.0.0.1 rec1.next.example.domain.xyz +short") != "1.2.3.5"

    assert host.check_output("dig @127.0.0.1 rec2.next.example.domain.xyz +short|head -n1") == "alias.next.example.domain.xyz."
    assert host.check_output("dig @127.0.0.1 rec3.next.example.domain.xyz +short|head -n1") == "wp.pl."

def test_forwarders_configuration(host):
    assert host.ansible(
      "shell",
      r"""cat /etc/named.conf |sed '/zone "other.example.domain.xyz" /,/}/p;d'|grep -E "forwarders {([0-9]{1,3}\\.){3}[0-9]{1,3} port 1234; ([0-9]{1,3}\\.){3}[0-9]{1,3} port 1234; };" """,
      become=True,
      check=False,
    )["stdout"]

    assert not host.ansible(
      "shell",
      """cat /etc/named.conf |sed '/zone "other.example.domain.xyz" /,/}/p;d'|grep -E "forwarders {([0-9]{1,3}\\.){3}[0-9]{1,3} port 1234; ([0-9]{1,3}\\.){3}[0-9]{1,3} port 1235; };" """,
      become=True,
      check=False,
    )["stdout"]
def test_ports_responses(host):
    host.ansible(
        "command",
        "yum install -y bind-utils",
    become=True,
    check=False,
    )
    assert host.check_output("dig @127.0.0.1 test.some.example.domain.xyz +short")
    assert host.check_output("dig @127.0.0.1 -p 5553 test.some.example.domain.xyz +short")
    assert host.run("dig @127.0.0.1 -p 5554 test.some.example.domain.xyz +short +timeout=1").failed
