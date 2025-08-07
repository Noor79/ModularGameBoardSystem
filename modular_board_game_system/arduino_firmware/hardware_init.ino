#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PN532.h>
#include "config.h"
#include "structures.h"
#include "utility.ino"

// System arrays (declared in main.ino, extern here)
extern ReaderConfig readers[MAX_READERS];
extern uint8_t numActiveReaders;

/**
 * Initialize all RFID readers
 */
void initializeReaders() {
  Serial.println("Initializing RFID readers...");
  
  for (uint8_t i = 0; i < numActiveReaders; i++) {
    selectMuxChannel(readers[i].muxAddress, readers[i].muxChannel);
    delay(MUX_SWITCH_DELAY);
    
    readers[i].reader = new Adafruit_PN532(-1, -1, &Wire);
    readers[i].reader->begin();
    delay(10);
    
    uint32_t versiondata = readers[i].reader->getFirmwareVersion();
    if (versiondata) {
      readers[i].reader->SAMConfig();
      readers[i].isActive = true;
      Serial.print("✅ Reader ");
      Serial.print(i);
      Serial.print(" (");
      Serial.print(readers[i].position);
      Serial.println(") initialized");
    } else {
      readers[i].isActive = false;
      Serial.print("❌ Reader ");
      Serial.print(i);
      Serial.print(" (");
      Serial.print(readers[i].position);
      Serial.println(") not found");
    }
  }
  
  Serial.print("Initialization complete. Active readers: ");
  uint8_t activeCount = 0;
  for (uint8_t i = 0; i < numActiveReaders; i++) {
    if (readers[i].isActive) activeCount++;
  }
  Serial.println(activeCount);
}


