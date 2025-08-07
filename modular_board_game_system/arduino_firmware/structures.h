#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <Arduino.h>
#include <Adafruit_PN532.h>

// ======================
// SYSTEM STATE STRUCTURES
// ======================
struct ReaderConfig {
  uint8_t muxAddress;           // I2C address of multiplexer
  uint8_t muxChannel;           // Channel on multiplexer (0-7)
  char position[4];             // Position notation (e.g., "a1", "b2")
  bool isActive;                // Whether this reader is connected and working
  Adafruit_PN532* reader;       // Pointer to PN532 instance
};

struct TagState {
  uint8_t uid[7];               // RFID tag UID
  uint8_t uidLength;            // Length of UID
  int8_t currentReader;         // Current reader index (-1 if not on board)
  int8_t lastReader;            // Last known reader index
  uint8_t missCount;            // Consecutive misses on current reader
  bool hasBeenPlaced;           // Whether tag has ever been placed on board
};

#endif


