import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cli_isis_data

mock_data_xr = {"cisco_xr": ["""
RP/0/RP0/CPU0:ROUTER-X1#show isis database verbose 
Tue Aug 17 12:30:51.498 AEST

IS-IS 1234 (Level-2) Link State Database
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd  ATT/P/OL
ROUTER-X1.00-00      * 0x00000832   0x74bc        64943/*            0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0xcc
  Router ID:      10.211.1.1
  Hostname:       ROUTER-X1
  Metric: 0          IP-Extended 10.211.1.1/32
    Prefix Attribute Flags: X:1 R:0 N:0 E:0 A:0
  Metric: 16777214   IS-Extended ROUTER-X2.00
    Local Interface ID: 9, Remote Interface ID: 50
    Interface IP Address: 10.123.0.17
    Neighbor IP Address: 10.123.0.18
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 1000
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
  Metric: 802        IS-Extended ROUTER-X5.00
    Local Interface ID: 7, Remote Interface ID: 53
    Interface IP Address: 10.123.0.25
    Neighbor IP Address: 10.123.0.26
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 802
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
ROUTER-X2.00-00        0x00000826   0x4390        65258/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0xcc
  Router ID:      10.211.1.2
  Hostname:       ROUTER-X2
  Metric: 0          IP-Extended 10.211.1.2/32
    Prefix Attribute Flags: X:1 R:0 N:0 E:0 A:0
  Metric: 301        IS-Extended ROUTER-X6.00
    Local Interface ID: 48, Remote Interface ID: 53
    Interface IP Address: 10.123.0.33
    Neighbor IP Address: 10.123.0.34
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 301
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
  Metric: 16777214   IS-Extended ROUTER-X1.00
    Local Interface ID: 50, Remote Interface ID: 9
    Interface IP Address: 10.123.0.18
    Neighbor IP Address: 10.123.0.17
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 1000
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
ROUTER-X5.00-00        0x00000830   0x59ed        64850/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0xcc
  IP Address:     10.211.0.5
  Router ID:      10.211.1.5
  Metric: 0          IP-Extended 10.211.0.5/32
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
    Source Router ID: 10.211.1.5
  Metric: 0          IP-Extended 10.211.1.5/32
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
    Source Router ID: 10.211.1.5
  Hostname:       ROUTER-X5
  Metric: 15         IS-Extended ROUTER-X6.00
    Local Interface ID: 58, Remote Interface ID: 55
    Interface IP Address: 10.123.0.29
    Neighbor IP Address: 10.123.0.30
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 15
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
  Metric: 802        IS-Extended ROUTER-X1.00
    Local Interface ID: 53, Remote Interface ID: 7
    Interface IP Address: 10.123.0.26
    Neighbor IP Address: 10.123.0.25
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 802
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
ROUTER-X6.00-00        0x00000828   0x3ce3        65298/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0xcc
  IP Address:     10.211.0.6
  Router ID:      10.211.1.6
  Metric: 0          IP-Extended 10.211.0.6/32
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
    Source Router ID: 10.211.1.6
  Metric: 0          IP-Extended 10.211.1.6/32
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
    Source Router ID: 10.211.1.6
  Hostname:       ROUTER-X6
  Metric: 15         IS-Extended ROUTER-X5.00
    Local Interface ID: 55, Remote Interface ID: 58
    Interface IP Address: 10.123.0.30
    Neighbor IP Address: 10.123.0.29
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 15
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec
  Metric: 301        IS-Extended ROUTER-X2.00
    Local Interface ID: 53, Remote Interface ID: 48
    Interface IP Address: 10.123.0.34
    Neighbor IP Address: 10.123.0.33
    Affinity: 0x00000000
    Physical BW: 10000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 301
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Physical BW: 10000000 kbits/sec

 Total Level-2 LSP count: 4     Local Level-2 LSP count: 1

IS-IS 4567 (Level-2) Link State Database
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd  ATT/P/OL
ROUTER-X1.00-00      * 0x0000153c   0xd242        64810/*            0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X1
  IPv6 Address:   fddd:2:c101::1
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c101::1/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:1::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:3::/36
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc::/36
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c101::1
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X5.00
    Local Interface ID: 68, Remote Interface ID: 57
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X2.00-00        0x00001534   0x53b2        65294/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X2
  IPv6 Address:   fddd:2:c101::2
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc::/36
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:2::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:3::/36
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c101::2/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c101::2
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X6.00
    Local Interface ID: 68, Remote Interface ID: 60
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X5.00-00        0x0000152c   0xfe31        65412/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X5
  IPv6 Address:   fddd:2:c201::1
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c201::1/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:2:1::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c201::1
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X1.00
    Local Interface ID: 57, Remote Interface ID: 68
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X7.00
    Local Interface ID: 64, Remote Interface ID: 102
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X6.00
    Local Interface ID: 60, Remote Interface ID: 62
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X6.00-00        0x00001527   0x2f57        64992/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X6
  IPv6 Address:   fddd:2:c201::2
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c201::2/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:2:2::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c201::2
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X2.00
    Local Interface ID: 60, Remote Interface ID: 68
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X8.00
    Local Interface ID: 64, Remote Interface ID: 102
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X5.00
    Local Interface ID: 62, Remote Interface ID: 60
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X7.00-00       0x0000151f   0xfe5b        65100/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X7
  IPv6 Address:   fddd:2:c301::1
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:2:3::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c301::1/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c301::1
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X5.00
    Local Interface ID: 102, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X8.00
    Local Interface ID: 103, Remote Interface ID: 103
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X8.00-00       0x0000152b   0xaf93        65180/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X8
  IPv6 Address:   fddd:2:c301::2
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c301::2/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
    Source Router ID: fddd:2:c301::2
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c301::2
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  MT:             IPv6 Unicast                                 0/0/0
  IPv6 Router ID: fddd:2:c301::2
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X6.00
    Local Interface ID: 102, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X7.00
    Local Interface ID: 103, Remote Interface ID: 103
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us

 Total Level-2 LSP count: 6     Local Level-2 LSP count: 1

IS-IS 8910 (Level-2) Link State Database
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd  ATT/P/OL
ROUTER-X1.00-00      * 0x00000824   0xf488        65487/*            0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X1
  IPv6 Address:   fddd:2:c101::1
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:1::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c101::1/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:2::/36
    Admin. Tag: 656
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c101::1
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X2.00
    Local Interface ID: 66, Remote Interface ID: 66
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X3.00
    Local Interface ID: 64, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X2.00-00        0x00000826   0x564c        65476/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X2
  IPv6 Address:   fddd:2:c101::2
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:2::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:2:c101::2/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:2::/36
    Admin. Tag: 656
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:2:c101::2
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X1.00
    Local Interface ID: 66, Remote Interface ID: 66
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X4.00
    Local Interface ID: 64, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X3.00-00        0x0000082d   0x4896        65368/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X3
  IPv6 Address:   fddd:3:c101::1
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:3::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:3::/36
    Admin. Tag: 656
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:3:c101::1/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:3:c101::1
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X1.00
    Local Interface ID: 64, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X4.00
    Local Interface ID: 66, Remote Interface ID: 66
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0
ROUTER-X4.00-00        0x00000829   0xc093        64822/65535        0/0/0
  Auth:           Algorithm HMAC-MD5, Length: 17
  Area Address:   49.1234
  NLPID:          0x8e
  Hostname:       ROUTER-X4
  IPv6 Address:   fddd:3:c101::2
  Metric: 1          MT (IPv6 Unicast) IPv6 fddc:0:4::/48
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6-Ext-InAr fddc:3::/36
    Admin. Tag: 656
    Prefix Attribute Flags: X:0 R:0 N:0 E:0 A:0
  Metric: 0          MT (IPv6 Unicast) IPv6 fddd:3:c101::2/128
    Prefix Attribute Flags: X:0 R:0 N:1 E:0 A:0
  Router Cap:     0.0.0.0 D:0 S:0
    IPv6 Router ID: fddd:3:c101::2
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
      Algorithm: 128
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X2.00
    Local Interface ID: 64, Remote Interface ID: 64
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  Metric: 10         MT (IPv6 Unicast) IS-Extended ROUTER-X3.00
    Local Interface ID: 66, Remote Interface ID: 66
    Physical BW: 10000000 kbits/sec
    Link Average Delay: 1 us
    Link Min/Max Delay: 1/1 us
    Link Delay Variation: 0 us
  MT:             IPv6 Unicast                                 0/0/0

 Total Level-2 LSP count: 4     Local Level-2 LSP count: 1
RP/0/RP0/CPU0:ROUTER-X1# 
    """]
}
    
def test_cli_isis_yed_data_dict_base():
    config = {}
    drawing = create_yed_diagram()
    drawer = cli_isis_data(drawing, config)
    drawer.work(mock_data_xr)
    drawer.drawing.dump_file(filename="test_cli_isis_yed_data_dict_base.graphml", folder="./Output/")
    # with open ("./Output/test_isis_drawer_yed_data_dict_base.graphml") as produced:
    #     with open("./Output/should_be_test_isis_drawer_yed_data_dict_base.graphml") as should_be:
    #         assert produced.read() == should_be.read()
            
# test_cli_isis_yed_data_dict_base()

