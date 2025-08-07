#include <Wire.h>
#include <Adafruit_PN532.h>
#include "config.h"
#include "structures.h"

// System arrays (declared in main.ino, extern here)
extern ReaderConfig readers[MAX_READERS];
extern TagState tagStates[MAX_READERS];
extern uint8_t numActiveReaders;
extern uint8_t numKnownTags;

/**
 * Select a specific channel on a multiplexer
 */
void selectMuxChannel(uint8_t muxAddress, uint8_t channel) {
  Wire.beginTransmission(muxAddress);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

/**
 * Find tag index by UID
 */
int8_t findTagByUID(uint8_t* uid, uint8_t uidLength) {
  for (uint8_t i = 0; i < numKnownTags; i++) {
    if (tagStates[i].uidLength == uidLength && 
        memcmp(tagStates[i].uid, uid, uidLength) == 0) {
      return i;
    }
  }
  return -1;
}

/**
 * Register a new tag in the system
 */
int8_t registerNewTag(uint8_t* uid, uint8_t uidLength) {
  if (numKnownTags >= MAX_READERS) {
    return -1; // No space for more tags
  }
  
  int8_t tagIndex = numKnownTags++;
  memcpy(tagStates[tagIndex].uid, uid, uidLength);
  tagStates[tagIndex].uidLength = uidLength;
  tagStates[tagIndex].currentReader = -1;
  tagStates[tagIndex].lastReader = -1;
  tagStates[tagIndex].missCount = 0;
  tagStates[tagIndex].hasBeenPlaced = false;
  
  return tagIndex;
}

/**
 * Convert UID to hex string for communication
 */
void uidToHexString(uint8_t* uid, uint8_t uidLength, char* hexString) {
  for (uint8_t i = 0; i < uidLength; i++) {
    sprintf(hexString + (i * 2), "%02X", uid[i]);
  }
  hexString[uidLength * 2] = '\0';
}

/**
 * Send standardized message to server
 */
void sendMessage(const char* action, int8_t tagIndex, int8_t readerIndex, int8_t fromReader = -1) {
  char uidHex[15]; // Max 7 bytes * 2 + null terminator
  uidToHexString(tagStates[tagIndex].uid, tagStates[tagIndex].uidLength, uidHex);
  
  if (strcmp(action, "LIFT") == 0) {
    Serial.print("LIFT:");
    Serial.print(uidHex);
    Serial.print(":");
    Serial.println(readers[readerIndex].position);
  } else if (strcmp(action, "PLACE") == 0) {
    Serial.print("PLACE:");
    Serial.print(uidHex);
    Serial.print(":");
    Serial.println(readers[readerIndex].position);
  } else if (strcmp(action, "MOVE") == 0 && fromReader >= 0) {
    Serial.print("MOVE:");
    Serial.print(uidHex);
    Serial.print(":");
    Serial.print(readers[fromReader].position);
    Serial.print(":");
    Serial.println(readers[readerIndex].position);
  }
}


