#include <Wire.h>
#include <Adafruit_PN532.h>

#include "config.h"
#include "structures.h"
#include "utility.ino"
#include "configuration.ino"
#include "hardware_init.ino"

// ======================
// GLOBAL SYSTEM STATE
// ======================
uint8_t muxAddresses[MAX_MULTIPLEXERS] = {0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77};
ReaderConfig readers[MAX_READERS];
TagState tagStates[MAX_READERS];
uint8_t numActiveReaders = 0;
uint8_t numKnownTags = 0;

// ======================
// MAIN FUNCTIONS
// ======================

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  Serial.println("=== Modulärt Brädspelssystem v1.0 ===");
  Serial.println("Initializing system...");
  
  // Initialize configuration
  initializeDefaultConfig();
  
  // Initialize hardware
  initializeReaders();
  
  Serial.println("System ready. Waiting for tags...");
  Serial.println("Send CONFIG commands to customize setup.");
}

void loop() {
  // Process serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil("\n");
    processConfigCommand(command);
  }
  
  // Scan all active readers
  for (uint8_t readerIndex = 0; readerIndex < numActiveReaders; readerIndex++) {
    if (!readers[readerIndex].isActive) {
      continue;
    }
    
    // Select reader
    selectMuxChannel(readers[readerIndex].muxAddress, readers[readerIndex].muxChannel);
    delay(SCAN_DELAY);
    
    // Try to read tag
    uint8_t uid[7];
    uint8_t uidLength = 0;
    bool tagPresent = readers[readerIndex].reader->readPassiveTargetID(
      PN532_MIFARE_ISO14443A, uid, &uidLength, 20);
    
    if (tagPresent) {
      // Tag detected
      int8_t tagIndex = findTagByUID(uid, uidLength);
      
      if (tagIndex < 0) {
        // New tag - register it
        tagIndex = registerNewTag(uid, uidLength);
        if (tagIndex < 0) {
          continue; // Failed to register (system full)
        }
      }
      
      TagState& tag = tagStates[tagIndex];
      tag.missCount = 0;
      
      // Determine event type
      if (tag.currentReader < 0) {
        // Tag placed on board
        if (!tag.hasBeenPlaced) {
          // First placement
          sendMessage("PLACE", tagIndex, readerIndex);
          tag.hasBeenPlaced = true;
        } else {
          // Placement after lift
          sendMessage("MOVE", tagIndex, readerIndex, tag.lastReader);
        }
        tag.currentReader = readerIndex;
      } else if (tag.currentReader != readerIndex) {
        // Tag moved to different reader
        sendMessage("MOVE", tagIndex, readerIndex, tag.currentReader);
        tag.lastReader = tag.currentReader;
        tag.currentReader = readerIndex;
      }
      // If tag.currentReader == readerIndex, tag is stationary (no action needed)
      
    } else {
      // No tag detected - check if we need to register a lift
      for (uint8_t tagIndex = 0; tagIndex < numKnownTags; tagIndex++) {
        TagState& tag = tagStates[tagIndex];
        
        if (tag.currentReader == readerIndex) {
          tag.missCount++;
          
          if (tag.missCount >= MISS_THRESHOLD) {
            // Tag lifted
            sendMessage("LIFT", tagIndex, readerIndex);
            tag.lastReader = tag.currentReader;
            tag.currentReader = -1;
            tag.missCount = 0;
          }
          break; // Only one tag can be on a reader at a time
        }
      }
    }
    
    delay(SCAN_DELAY);
  }
}


