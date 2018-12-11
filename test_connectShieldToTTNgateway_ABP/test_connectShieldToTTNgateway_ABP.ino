#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

//#define MAX_CHANNELS;
//#define MAX_BANDS;
//#define LIMIT_CHANNELS;
//#define BAND_MILLI;
//#define BAND_CENTI;
//#define BAND_DECI;
//#define BAND_AUX;
//#define CFG_sx1276_radio 1
////#define LMIC_USE_INTERRUPTS
//#define LMIC_DEBUG_LEVEL 2
//#define USE_ORIGINAL_AES
////#define USE_IDEETRON_AES


//void setup() {
//  LMIC_setupBand();
//}

// LoRaWAN NwkSKey, network session key
//static const PROGMEM u1_t NWKSKEY[16] = { 0x81, 0x9C, 0x7D, 0xD1, 0x77, 0xC4, 0xBE, 0x5F, 0x03, 0xB8, 0x86, 0x24, 0xDE, 0xF1, 0xD8, 0x70 };
static const PROGMEM u1_t NWKSKEY[16] = { 0xFD, 0x8D, 0xBC, 0xF9, 0x59, 0x9B, 0xFE, 0x4E, 0x3D, 0xA4, 0xB6, 0x00, 0x29, 0x1E, 0x35, 0x2C }; // lora_node_gps_abp

// LoRaWAN AppSKey, application session key
static const u1_t PROGMEM APPSKEY[16] = { 0x50, 0x72, 0x66, 0x9D, 0xFB, 0xC2, 0xBC, 0x31, 0x24, 0x92, 0xC7, 0x1F, 0x69, 0x39, 0x95, 0x6E };  // lora_node_gps_abp
// static const u1_t PROGMEM APPSKEY[16] = { 0x53, 0x2C, 0x9A, 0x24, 0x46, 0x39, 0x04, 0x52, 0x1B, 0xE3, 0x74, 0x8F, 0xAD, 0x4E, 0xBE, 0x45 };
// static const u1_t PROGMEM APPSKEY[16] = { 0x35, 0xC2, 0xA9, 0x42, 0x64, 0x93, 0x40, 0x25, 0xB1, 0x3E, 0x47, 0xF8, 0xDA, 0xE4, 0xEB, 0x54 };

// LoRaWAN end-device address (DevAddr)
static const u4_t DEVADDR = { 0x26011AEF };

// These callbacks are only used in over-the-air activation, so they are
// left empty here (we cannot leave them out completely unless
// DISABLE_JOIN is set in config.h, otherwise the linker will complain).
void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

static uint8_t mydata[] = "hello";
static osjob_t sendjob;

// Schedule data trasmission in every this many seconds (might become longer due to duty
// cycle limitations).
// we set 10 seconds interval
const unsigned TX_INTERVAL = 10;

// Pin mapping according to Cytron LoRa Shield RFM
const lmic_pinmap lmic_pins = {
  .nss = 10,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 7,
  .dio = {2, 5, 6},
};

void onEvent (ev_t ev) {
  Serial.print(os_getTime());
  Serial.print(": ");
  switch (ev) {
    case EV_SCAN_TIMEOUT:
      Serial.println(F("EV_SCAN_TIMEOUT"));
      break;
    case EV_BEACON_FOUND:
      Serial.println(F("EV_BEACON_FOUND"));
      break;
    case EV_BEACON_MISSED:
      Serial.println(F("EV_BEACON_MISSED"));
      break;
    case EV_BEACON_TRACKED:
      Serial.println(F("EV_BEACON_TRACKED"));
      break;
    case EV_JOINING:
      Serial.println(F("EV_JOINING"));
      break;
    case EV_JOINED:
      Serial.println(F("EV_JOINED"));
      break;
    case EV_RFU1:
      Serial.println(F("EV_RFU1"));
      break;
    case EV_JOIN_FAILED:
      Serial.println(F("EV_JOIN_FAILED"));
      break;
    case EV_REJOIN_FAILED:
      Serial.println(F("EV_REJOIN_FAILED"));
      break;
    case EV_TXCOMPLETE:
      Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
      if (LMIC.dataLen) {
        // data received in rx slot after tx
        Serial.print(F("Data Received: "));
        Serial.write(LMIC.frame + LMIC.dataBeg, LMIC.dataLen);
        Serial.println();
      }
      // Schedule next transmission
      os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
      break;
    case EV_LOST_TSYNC:
      Serial.println(F("EV_LOST_TSYNC"));
      break;
    case EV_RESET:
      Serial.println(F("EV_RESET"));
      break;
    case EV_RXCOMPLETE:
      // data received in ping slot
      Serial.println(F("EV_RXCOMPLETE"));
      break;
    case EV_LINK_DEAD:
      Serial.println(F("EV_LINK_DEAD"));
      break;
    case EV_LINK_ALIVE:
      Serial.println(F("EV_LINK_ALIVE"));
      break;
    default:
      Serial.println(F("Unknown event"));
      Serial.println(ev);
      break;
  }
}

void do_send(osjob_t* j) {
  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {
    // Prepare upstream data transmission at the next possible time.
    LMIC_setTxData2(1, mydata, sizeof(mydata) - 1, 0);
    Serial.println(F("Packet queued"));
  }
  // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
  Serial.begin(115200);
  Serial.println(F("Starting"));

  // LMIC init
  os_init();

  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // Set static session parameters. Instead of dynamically establishing a session
  // by joining the network, precomputed session parameters are be provided.
  uint8_t appskey[sizeof(APPSKEY)];
  uint8_t nwkskey[sizeof(NWKSKEY)];
  memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
  memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
  LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);

  // Select frequencies range
  //LMIC_selectSubBand(3);

  // Disable link check validation
  LMIC_setLinkCheckMode(0);

  // Disable ADR
  LMIC_setAdrMode(false);

  // TTN uses SF9 for its RX2 window.
  LMIC.dn2Dr = DR_SF9;

  // Set data rate and transmit power for uplink (note: txpow seems to be ignored by the library)
  LMIC_setDrTxpow(DR_SF7, 14);



  #if defined(CFG_eu868)
    // Set up the channels used by the Things Network, which corresponds
    // to the defaults of most gateways. Without this, only three base
    // channels from the LoRaWAN specification are used, which certainly
    // works, so it is good for debugging, but can overload those
    // frequencies, so be sure to configure the full frequency range of
    // your network here (unless your network autoconfigures them).
    // Setting up channels should happen after LMIC_setSession, as that
    // configures the minimal channel set.
  LMIC_setupChannel(0, 868100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(1, 868300000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);      // g-band
  LMIC_setupChannel(2, 868500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(3, 867100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(4, 867300000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(5, 867500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(6, 867700000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(7, 867900000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(8, 868800000, DR_RANGE_MAP(DR_FSK,  DR_FSK),  BAND_MILLI);      // g2-band
  // TTN defines an additional channel at 869.525Mhz using SF9 for class B
  // devices' ping slots. LMIC does not have an easy way to define set this
  // frequency and support for class B is spotty and untested, so this
  // frequency is not configured here.
#elif defined(CFG_us915)
  // NA-US channels 0-71 are configured automatically
  // but only one group of 8 should (a subband) should be active
  // TTN recommends the second sub band, 1 in a zero based count.
  // https://github.com/TheThingsNetwork/gateway-conf/blob/master/US-global_conf.json
  LMIC_selectSubBand(1);
#endif



  // Start job
  do_send(&sendjob);
}

void loop() {
  os_runloop_once();
}
