# this nftable config is just for personal use
# and reason of why I upload it on github is that I wanna have
# access to it from internet(everywhere)

print("\nMAKE SURE U R ROOT\n")
my_ip = input("enter ip for my_ip var : ")
gateway = input("enter gateway for dg var : ")
conf = """
define my_ip = %s
define gateway = %s

table inet filter {
    chain input {
        type filter hook input priority filter
        tcp flags 0x02 drop
        ip daddr $my_ip icmp type echo-request drop
        ip daddr $my_ip igmp type 0x11 drop
        ip protocol udp drop
        ip protocol udp drop
        ip daddr $gateway udp sport {0-65535} accept
        ip saddr $gateway udp dport {0-65535} accept
        }
    }
""" % (my_ip, gateway)
ok = input("\n this the config :\n" + conf + "\n\nok and continue[y/N]? ")
if ok.lower() == "n" : sys.exit()
with open ("/etc/nftables.conf", "w") as config :
    config.write(conf)
print("\nDONE\n")
