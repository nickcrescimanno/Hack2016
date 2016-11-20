#pragma once

/////////////
// LINKING //
/////////////
#pragma comment(lib, "XInput.lib")   // Library. If your compiler doesn't support this type of lib include change to the corresponding one

//////////////
// INCLUDES //
//////////////
#define WIN32_LEAN_AND_MEAN // We don't want the extra stuff like MFC and such
#include <Windows.h>
#include <XInput.h>     // XInput API

#include "GamepadState.h"

#define SECRET_XINPUT
#ifdef SECRET_XINPUT
#define XINPUT_GAMEPAD_GUIDE 0x400
#endif

namespace Hack2016
{
	class Gamepad
	{
	private:
		XINPUT_STATE mControllerXState;
		unsigned __int32 mControllerNum;
		GamepadState mState;

	#ifdef SECRET_XINPUT
		HINSTANCE hGetProcIDDLL;
		//typedef the function. It takes an int and a pointer to a ControllerStruct and returns an error code
		//as an int.  it's 0 for no error and 1167 for "controller not present".  presumably there are others
		//but I never saw them.  It won't cause a crash on error, it just won't update the data.
		typedef DWORD(__stdcall * pICFUNC)(DWORD, XINPUT_STATE * const);
		pICFUNC getControllerData;
	#endif

	public:
		Gamepad(unsigned __int32 const);
		~Gamepad();

		bool IsConnected(void);

		void Update(void);

		GamepadState const GetState(void) { return mState; }

		void SetVibrartion(float left = 0.0f, float right = 0.0f);
	};
}