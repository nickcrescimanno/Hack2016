#pragma once

#define GAMEPAD_A 0x01
#define GAMEPAD_B 0x02
#define GAMEPAD_X 0x04
#define GAMEPAD_Y 0x08
#define GAMEPAD_DPAD_UP		0x10
#define GAMEPAD_DPAD_DOWN	0x20
#define GAMEPAD_DPAD_LEFT	0x40
#define GAMEPAD_DPAD_RIGHT	0x80

#define GAMEPAD_BYTES 8

namespace Hack2016
{
	struct GamepadState
	{
		union
		{
			unsigned __int64	_RAW;	// RAW data
			unsigned __int8		_ARRAY[8];	// Data as array of uint8
			struct{
				unsigned __int8 LX;				// Left Thumstick X
				unsigned __int8 LY;				// Left Thumstick Y
				unsigned __int8 RX;				// Right Thumstick X
				unsigned __int8 RY;				// Right Thumstick Y
				unsigned __int8 LT;		// Left Trigger
				unsigned __int8 RT;		// Right Trigger
				unsigned __int8 B;		// Buttons
				unsigned __int8 CS;		// Checksum
			};
		};
	};

}