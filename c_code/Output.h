#pragma once

#include <thread>
#include "nout.h"
#include "Gamepad.h"
#include "GamepadState.h"

#define SAMPLE_RATE 8000
#define GAMEPAD_SLEEP 100

namespace Hack2016
{
	class Output
	{
	private:
		nout * pSignal;
		Gamepad * pGamepad;
		GamepadState oldState;
		std::thread * pThread;
	
	public:
		Output();
		~Output();

		GamepadState const GetState(void) { return pGamepad->GetState(); }

		void Update(void);

		void Run(void);
		void Stop(void);
	};
}
