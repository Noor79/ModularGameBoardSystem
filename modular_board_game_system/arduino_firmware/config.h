#ifndef CONFIG_H
#define CONFIG_H

// ======================
// SYSTEM CONFIGURATION
// ======================
#define MAX_READERS 64           // Maximum number of supported readers
#define MAX_MULTIPLEXERS 8       // Maximum number of I2C multiplexers
#define CHANNELS_PER_MUX 8       // Channels per multiplexer
#define MISS_THRESHOLD 12        // Miss count before registering a lift
#define SCAN_DELAY 10           // Delay between sensor scans (ms)
#define MUX_SWITCH_DELAY 50     // Delay when switching multiplexer channels (ms)

// Default multiplexer addresses (can be configured via serial)
extern uint8_t muxAddresses[MAX_MULTIPLEXERS];

#endif


