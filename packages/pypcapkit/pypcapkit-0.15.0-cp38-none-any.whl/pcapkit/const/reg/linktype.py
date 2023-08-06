# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Link-Layer Header Type Values"""

from aenum import IntEnum, extend_enum

__all__ = ['LinkType']


class LinkType(IntEnum):
    """[LinkType] Link-Layer Header Type Values"""

    _ignore_ = 'LinkType _'
    LinkType = vars()

    #: ``DLT_NULL``
    LinkType['NULL'] = 0

    #: ``DLT_EN10MB``
    LinkType['ETHERNET'] = 1

    #: ``DLT_AX25``
    LinkType['AX25'] = 3

    #: ``DLT_IEEE802``
    LinkType['IEEE802_5'] = 6

    #: ``DLT_ARCNET``
    LinkType['ARCNET_BSD'] = 7

    #: ``DLT_SLIP``
    LinkType['SLIP'] = 8

    #: ``DLT_PPP``
    LinkType['PPP'] = 9

    #: ``DLT_FDDI``
    LinkType['FDDI'] = 10

    #: ``DLT_PPP_SERIAL``
    LinkType['PPP_HDLC'] = 50

    #: ``DLT_PPP_ETHER``
    LinkType['PPP_ETHER'] = 51

    #: ``DLT_ATM_RFC1483``
    LinkType['ATM_RFC1483'] = 100

    #: ``DLT_RAW``
    LinkType['RAW'] = 101

    #: ``DLT_C_HDLC``
    LinkType['C_HDLC'] = 104

    #: ``DLT_IEEE802_11``
    LinkType['IEEE802_11'] = 105

    #: ``DLT_FRELAY``
    LinkType['FRELAY'] = 107

    #: ``DLT_LOOP``
    LinkType['LOOP'] = 108

    #: ``DLT_LINUX_SLL``
    LinkType['LINUX_SLL'] = 113

    #: ``DLT_LTALK``
    LinkType['LTALK'] = 114

    #: ``DLT_PFLOG``
    LinkType['PFLOG'] = 117

    #: ``DLT_PRISM_HEADER``
    LinkType['IEEE802_11_PRISM'] = 119

    #: ``DLT_IP_OVER_FC``
    LinkType['IP_OVER_FC'] = 122

    #: ``DLT_SUNATM``
    LinkType['SUNATM'] = 123

    #: ``DLT_IEEE802_11_RADIO``
    LinkType['IEEE802_11_RADIOTAP'] = 127

    #: ``DLT_ARCNET_LINUX``
    LinkType['ARCNET_LINUX'] = 129

    #: ``DLT_APPLE_IP_OVER_IEEE1394``
    LinkType['APPLE_IP_OVER_IEEE1394'] = 138

    #: ``DLT_MTP2_WITH_PHDR``
    LinkType['MTP2_WITH_PHDR'] = 139

    #: ``DLT_MTP2``
    LinkType['MTP2'] = 140

    #: ``DLT_MTP3``
    LinkType['MTP3'] = 141

    #: ``DLT_SCCP``
    LinkType['SCCP'] = 142

    #: ``DLT_DOCSIS``
    LinkType['DOCSIS'] = 143

    #: ``DLT_LINUX_IRDA``
    LinkType['LINUX_IRDA'] = 144

    #: ``DLT_USER0``
    LinkType['USER0'] = 147

    #: ``DLT_USER1``
    LinkType['USER1'] = 148

    #: ``DLT_USER2``
    LinkType['USER2'] = 149

    #: ``DLT_USER3``
    LinkType['USER3'] = 150

    #: ``DLT_USER4``
    LinkType['USER4'] = 151

    #: ``DLT_USER5``
    LinkType['USER5'] = 152

    #: ``DLT_USER6``
    LinkType['USER6'] = 153

    #: ``DLT_USER7``
    LinkType['USER7'] = 154

    #: ``DLT_USER8``
    LinkType['USER8'] = 155

    #: ``DLT_USER9``
    LinkType['USER9'] = 156

    #: ``DLT_USER10``
    LinkType['USER10'] = 157

    #: ``DLT_USER11``
    LinkType['USER11'] = 158

    #: ``DLT_USER12``
    LinkType['USER12'] = 159

    #: ``DLT_USER13``
    LinkType['USER13'] = 160

    #: ``DLT_USER14``
    LinkType['USER14'] = 161

    #: ``DLT_USER15``
    LinkType['USER15'] = 162

    #: ``DLT_IEEE802_11_RADIO_AVS``
    LinkType['IEEE802_11_AVS'] = 163

    #: ``DLT_BACNET_MS_TP``
    LinkType['BACNET_MS_TP'] = 165

    #: ``DLT_PPP_PPPD``
    LinkType['PPP_PPPD'] = 166

    #: ``DLT_GPRS_LLC``
    LinkType['GPRS_LLC'] = 169

    #: ``DLT_GPF_T``
    LinkType['GPF_T'] = 170

    #: ``DLT_GPF_F``
    LinkType['GPF_F'] = 171

    #: ``DLT_LINUX_LAPD``
    LinkType['LINUX_LAPD'] = 177

    #: ``DLT_MFR``
    LinkType['MFR'] = 182

    #: ``DLT_BLUETOOTH_HCI_H4``
    LinkType['BLUETOOTH_HCI_H4'] = 187

    #: ``DLT_USB_LINUX``
    LinkType['USB_LINUX'] = 189

    #: ``DLT_PPI``
    LinkType['PPI'] = 192

    #: ``DLT_IEEE802_15_4_WITHFCS``
    LinkType['IEEE802_15_4_WITHFCS'] = 195

    #: ``DLT_SITA``
    LinkType['SITA'] = 196

    #: ``DLT_ERF``
    LinkType['ERF'] = 197

    #: ``DLT_BLUETOOTH_HCI_H4_WITH_PHDR``
    LinkType['BLUETOOTH_HCI_H4_WITH_PHDR'] = 201

    #: ``DLT_AX25_KISS``
    LinkType['AX25_KISS'] = 202

    #: ``DLT_LAPD``
    LinkType['LAPD'] = 203

    #: ``DLT_PPP_WITH_DIR``
    LinkType['PPP_WITH_DIR'] = 204

    #: ``DLT_C_HDLC_WITH_DIR``
    LinkType['C_HDLC_WITH_DIR'] = 205

    #: ``DLT_FRELAY_WITH_DIR``
    LinkType['FRELAY_WITH_DIR'] = 206

    #: ``DLT_LAPB_WITH_DIR``
    LinkType['LAPB_WITH_DIR'] = 207

    #: ``DLT_IPMB_LINUX``
    LinkType['IPMB_LINUX'] = 209

    #: ``DLT_IEEE802_15_4_NONASK_PHY``
    LinkType['IEEE802_15_4_NONASK_PHY'] = 215

    #: ``DLT_USB_LINUX_MMAPPED``
    LinkType['USB_LINUX_MMAPPED'] = 220

    #: ``DLT_FC_2``
    LinkType['FC_2'] = 224

    #: ``DLT_FC_2_WITH_FRAME_DELIMS``
    LinkType['FC_2_WITH_FRAME_DELIMS'] = 225

    #: ``DLT_IPNET``
    LinkType['IPNET'] = 226

    #: ``DLT_CAN_SOCKETCAN``
    LinkType['CAN_SOCKETCAN'] = 227

    #: ``DLT_IPV4``
    LinkType['IPV4'] = 228

    #: ``DLT_IPV6``
    LinkType['IPV6'] = 229

    #: ``DLT_IEEE802_15_4_NOFCS``
    LinkType['IEEE802_15_4_NOFCS'] = 230

    #: ``DLT_DBUS``
    LinkType['DBUS'] = 231

    #: ``DLT_DVB_CI``
    LinkType['DVB_CI'] = 235

    #: ``DLT_MUX27010``
    LinkType['MUX27010'] = 236

    #: ``DLT_STANAG_5066_D_PDU``
    LinkType['STANAG_5066_D_PDU'] = 237

    #: ``DLT_NFLOG``
    LinkType['NFLOG'] = 239

    #: ``DLT_NETANALYZER``
    LinkType['NETANALYZER'] = 240

    #: ``DLT_NETANALYZER_TRANSPARENT``
    LinkType['NETANALYZER_TRANSPARENT'] = 241

    #: ``DLT_IPOIB``
    LinkType['IPOIB'] = 242

    #: ``DLT_MPEG_2_TS``
    LinkType['MPEG_2_TS'] = 243

    #: ``DLT_NG40``
    LinkType['NG40'] = 244

    #: ``DLT_NFC_LLCP``
    LinkType['NFC_LLCP'] = 245

    #: ``DLT_INFINIBAND``
    LinkType['INFINIBAND'] = 247

    #: ``DLT_SCTP``
    LinkType['SCTP'] = 248

    #: ``DLT_USBPCAP``
    LinkType['USBPCAP'] = 249

    #: ``DLT_RTAC_SERIAL``
    LinkType['RTAC_SERIAL'] = 250

    #: ``DLT_BLUETOOTH_LE_LL``
    LinkType['BLUETOOTH_LE_LL'] = 251

    #: ``DLT_NETLINK``
    LinkType['NETLINK'] = 253

    #: ``DLT_BLUETOOTH_LINUX_MONITOR``
    LinkType['BLUETOOTH_LINUX_MONITOR'] = 254

    #: ``DLT_BLUETOOTH_BREDR_BB``
    LinkType['BLUETOOTH_BREDR_BB'] = 255

    #: ``DLT_BLUETOOTH_LE_LL_WITH_PHDR``
    LinkType['BLUETOOTH_LE_LL_WITH_PHDR'] = 256

    #: ``DLT_PROFIBUS_DL``
    LinkType['PROFIBUS_DL'] = 257

    #: ``DLT_PKTAP``
    LinkType['PKTAP'] = 258

    #: ``DLT_EPON``
    LinkType['EPON'] = 259

    #: ``DLT_IPMI_HPM_2``
    LinkType['IPMI_HPM_2'] = 260

    #: ``DLT_ZWAVE_R1_R2``
    LinkType['ZWAVE_R1_R2'] = 261

    #: ``DLT_ZWAVE_R3``
    LinkType['ZWAVE_R3'] = 262

    #: ``DLT_WATTSTOPPER_DLM``
    LinkType['WATTSTOPPER_DLM'] = 263

    #: ``DLT_ISO_14443``
    LinkType['ISO_14443'] = 264

    #: ``DLT_RDS``
    LinkType['RDS'] = 265

    #: ``DLT_USB_DARWIN``
    LinkType['USB_DARWIN'] = 266

    #: ``DLT_SDLC``
    LinkType['SDLC'] = 268

    #: ``DLT_LORATAP``
    LinkType['LORATAP'] = 270

    #: ``DLT_VSOCK``
    LinkType['VSOCK'] = 271

    #: ``DLT_NORDIC_BLE``
    LinkType['NORDIC_BLE'] = 272

    #: ``DLT_DOCSIS31_XRA31``
    LinkType['DOCSIS31_XRA31'] = 273

    #: ``DLT_ETHERNET_MPACKET``
    LinkType['ETHERNET_MPACKET'] = 274

    #: ``DLT_DISPLAYPORT_AUX``
    LinkType['DISPLAYPORT_AUX'] = 275

    #: ``DLT_LINUX_SLL2``
    LinkType['LINUX_SLL2'] = 276

    #: ``DLT_OPENVIZSLA``
    LinkType['OPENVIZSLA'] = 278

    #: ``DLT_EBHSCR``
    LinkType['EBHSCR'] = 279

    #: ``DLT_VPP_DISPATCH``
    LinkType['VPP_DISPATCH'] = 280

    #: ``DLT_DSA_TAG_BRCM``
    LinkType['DSA_TAG_BRCM'] = 281

    #: ``DLT_DSA_TAG_BRCM_PREPEND``
    LinkType['DSA_TAG_BRCM_PREPEND'] = 282

    #: ``DLT_IEEE802_15_4_TAP``
    LinkType['IEEE802_15_4_TAP'] = 283

    #: ``DLT_DSA_TAG_DSA``
    LinkType['DSA_TAG_DSA'] = 284

    #: ``DLT_DSA_TAG_EDSA``
    LinkType['DSA_TAG_EDSA'] = 285

    #: ``DLT_ELEE``
    LinkType['ELEE'] = 286

    #: ``DLT_Z_WAVE_SERIAL``
    LinkType['Z_WAVE_SERIAL'] = 287

    #: ``DLT_USB_2_0``
    LinkType['USB_2_0'] = 288

    #: ``DLT_ATSC_ALP``
    LinkType['ATSC_ALP'] = 289

    @staticmethod
    def get(key, default=-1):
        """Backport support for original codes."""
        if isinstance(key, int):
            return LinkType(key)
        if key not in LinkType._member_map_:  # pylint: disable=no-member
            extend_enum(LinkType, key, default)
        return LinkType[key]

    @classmethod
    def _missing_(cls, value):
        """Lookup function used when value is not found."""
        if not (isinstance(value, int) and 0x00000000 <= value <= 0xFFFFFFFF):
            raise ValueError('%r is not a valid %s' % (value, cls.__name__))
        extend_enum(cls, 'Unassigned [%d]' % value, value)
        return cls(value)
