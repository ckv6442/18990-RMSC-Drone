// Includes necessary for this project
#include <Wire.h>
#include <PN532.h>
#include <PN532_I2C.h>
#include <NfcAdapter.h>

// Configure I2C device as NFC
PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);

// Setup the device
void setup(void) 
{
  // Connect to serial and print something
  Serial.begin(115200);
  Serial.println("Hello!");

  // Start the NFC devoce
  nfc.begin();

  // Get the firmware version of the NFC (not needed)
  // Used to confirm if the board is connected or not
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) 
  {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  
  // Got data, print it out
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX); 
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC); 
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
  
  // Set the max number of retry attempts to read from a card
  // This prevents us from waiting forever for a card, which is
  // the default behaviour of the PN532.
  nfc.setPassiveActivationRetries(0xFF);

  // configure board to read RFID tags
  nfc.SAMConfig();

  // Wait for RFID Tag
  Serial.println("Waiting for an ISO14443A card");
}
 
void loop(void) 
{
  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

  // 1 second delay, change here to be longer or shorter (maybe 0.5s?)
  delay(1000);

  // Read the passive target
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);

  // If a card was found
  if (success) {
    // Print the tag info
    /*
    Serial.println("Found a card!");
    Serial.print("UID Length: ");
    Serial.print(uidLength, DEC);
    Serial.println(" bytes");
    Serial.print("UID Value: ");
    */

    // Print the data on the card
    /*
    for (uint8_t i=0; i < uidLength; i++) 
    {
      Serial.print(" 0x");
      Serial.print(uid[i], HEX); 
    }
    Serial.println("");
    */

    // Print an identifier for the python term to read
    Serial.print("0x");
    Serial.print(PN532_I2C_ADDRESS, HEX);
    Serial.println("");
    
    // Wait 1 second before continuing
    delay(1000);
  }
  else
  {
    // PN532 probably timed out waiting for a card
    Serial.println("Timed out waiting for a card");
  }
}
