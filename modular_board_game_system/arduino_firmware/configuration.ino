#include <Arduino.h>
#include "config.h"
#include "structures.h"

// System arrays (declared in main.ino, extern here)
extern ReaderConfig readers[MAX_READERS];
extern uint8_t numActiveReaders;

/**
 * Initialize default board configuration (4x4 grid)
 */
void initializeDefaultConfig() {
  // Default 4x4 configuration
  const char* defaultPositions[16] = {
    "a4", "b4", "c4", "d4",
    "a3", "b3", "c3", "d3",
    "a2", "b2", "c2", "d2",
    "a1", "b1", "c1", "d1"
  };
  
  numActiveReaders = 16;
  
  for (uint8_t i = 0; i < numActiveReaders; i++) {
    readers[i].muxAddress = (i < 8) ? 0x70 : 0x71;
    readers[i].muxChannel = i % 8;
    strcpy(readers[i].position, defaultPositions[i]);
    readers[i].isActive = false;
    readers[i].reader = nullptr;
  }
}

/**
 * Process configuration commands from serial
 */
void processConfigCommand(String command) {
  command.trim();
  
  if (command.startsWith("CONFIG_READER:")) {
    // Format: CONFIG_READER:index:muxAddr:channel:position
    int firstColon = command.indexOf(":", 14);
    int secondColon = command.indexOf(":", firstColon + 1);
    int thirdColon = command.indexOf(":", secondColon + 1);
    
    if (firstColon > 0 && secondColon > 0 && thirdColon > 0) {
      uint8_t index = command.substring(14, firstColon).toInt();
      uint8_t muxAddr = strtol(command.substring(firstColon + 1, secondColon).c_str(), NULL, 16);
      uint8_t channel = command.substring(secondColon + 1, thirdColon).toInt();
      String position = command.substring(thirdColon + 1);
      
      if (index < MAX_READERS && position.length() <= 3) {
        readers[index].muxAddress = muxAddr;
        readers[index].muxChannel = channel;
        strcpy(readers[index].position, position.c_str());
        Serial.print("CONFIG_ACK:READER:");
        Serial.println(index);
      }
    }
  } else if (command == "CONFIG_RESET") {
    initializeDefaultConfig();
    Serial.println("CONFIG_ACK:RESET");
  } else if (command == "CONFIG_STATUS") {
    Serial.print("STATUS:READERS:");
    Serial.print(numActiveReaders);
    Serial.print(":TAGS:");
    Serial.println(numKnownTags);
  }
}


