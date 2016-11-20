#pragma once

#include "GamepadState.h"

namespace Hack2016
{
	struct Package
	{
		union {
			unsigned __int32	_RAW;		// RAW data
			unsigned __int8		_ARRAY[4];	// Data as array of uint8
			struct {
				unsigned __int8 LX;				// Left Thumstick X
				unsigned __int8 LY;				// Left Thumstick Y
				unsigned __int8 RT;		// Right Trigger
				unsigned __int8 B;		// Buttons
			};
		};

		static Package FromGamepadState(GamepadState const s)
		{
			Package p;
			p.LX = s.LX;
			p.LY = s.LY;
			p.RT = s.RT;
			p.B = s.B;
			return p;
		}
	};

}