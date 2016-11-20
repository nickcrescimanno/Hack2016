#include "Gamepad.h"
#include <cstdint>
#include <math.h>

namespace Hack2016{

	Gamepad::Gamepad(unsigned __int32 gamepadIndex)
		:mControllerNum(gamepadIndex)
	{
	#ifdef SECRET_XINPUT

			//First create an HINSTANCE of the [Xx][Ii]nput1_X.dll.  Probably should use system variables to find it
			//but whatever.
	#if WINVER==0x602	// Windows 8
			hGetProcIDDLL = LoadLibraryA("C:/Windows/System32/XInput1_4.dll");
	#else				// Older Windows
			hGetProcIDDLL = LoadLibraryA("C:/Windows/System32/xinput1_3.dll");
	#endif

			//Get the address of ordinal 100.
			FARPROC lpfnGetProcID = GetProcAddress(HMODULE(hGetProcIDDLL), (LPCSTR)100);

			//Assign it to getControllerData for easier use
			getControllerData = pICFUNC(lpfnGetProcID);

	#endif
	}


	Gamepad::~Gamepad()
	{
		SetVibrartion();

	#ifdef SECRET_XINPUT
		FreeLibrary(hGetProcIDDLL);
	#endif
	}

	void Gamepad::SetVibrartion(float left, float right)
	{
		// Create a new Vibration
		XINPUT_VIBRATION vibration;

		memset(&vibration, 0, sizeof(XINPUT_VIBRATION));

		int leftVib = (int)(left * 65535.0f);
		int rightVib = (int)(right * 65535.0f);

		// Set the vibartion values
		vibration.wLeftMotorSpeed = leftVib;
		vibration.wRightMotorSpeed = rightVib;
		// Vibrate the controller
		XInputSetState((int)mControllerNum, &vibration);
	}

	void Gamepad::Update(void)
	{
		// Clean the state
		memset(&mControllerXState, 0, sizeof(XINPUT_STATE));

		// Get the state
#ifdef SECRET_XINPUT
		DWORD result = getControllerData(mControllerNum, &mControllerXState);
#else
		DWORD result = XInputGetState(mControllerNum, &mControllerXState);
#endif

		// Reset mState
		mState._RAW = 0;

		if (result == ERROR_SUCCESS)
		{
#pragma region Success
			if (mControllerXState.Gamepad.bRightTrigger && mControllerXState.Gamepad.bRightTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
				mState.RT = mControllerXState.Gamepad.bRightTrigger;

			if (mControllerXState.Gamepad.bLeftTrigger && mControllerXState.Gamepad.bLeftTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
				mState.LT = mControllerXState.Gamepad.bLeftTrigger;

			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_A) mState.B |= GAMEPAD_A;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_B) mState.B |= GAMEPAD_B;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_X) mState.B |= GAMEPAD_X;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_Y) mState.B |= GAMEPAD_Y;

			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_UP) mState.B |= GAMEPAD_DPAD_UP;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_DOWN) mState.B |= GAMEPAD_DPAD_DOWN;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_LEFT) mState.B |= GAMEPAD_DPAD_LEFT;
			if (mControllerXState.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_RIGHT) mState.B |= GAMEPAD_DPAD_RIGHT;


#pragma region LeftThumbStick
			float thumbX = mControllerXState.Gamepad.sThumbLX;
			float thumbY = mControllerXState.Gamepad.sThumbLY;

			//determine how far the controller is pushed
			float magnitude = sqrt(thumbX*thumbX + thumbY*thumbY);

			//determine the direction the controller is pushed
			float normalizedX = thumbX / magnitude;
			float normalizedY = thumbY / magnitude;

			//check if the controller is outside a circular dead zone
			if (magnitude > XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE)
			{
				mState.LX = (mControllerXState.Gamepad.sThumbLX + INT16_MAX + 1) >> 8;//0.5f * (normalizedX + 1.0f) * INT8_MAX;
				mState.LY = (mControllerXState.Gamepad.sThumbLY + INT16_MAX + 1) >> 8;
			}
			else //if the controller is in the deadzone zero out the magnitude
			{
				mState.LX = UINT8_MAX >> 1;
				mState.LY = UINT8_MAX >> 1;
			}
#pragma endregion

#pragma region RightThumbStick
			thumbX = mControllerXState.Gamepad.sThumbRX;
			thumbY = mControllerXState.Gamepad.sThumbRY;

			//determine how far the controller is pushed
			magnitude = sqrt(thumbX*thumbX + thumbY*thumbY);

			//determine the direction the controller is pushed
			normalizedX = thumbX / magnitude;
			normalizedY = thumbY / magnitude;

			//check if the controller is outside a circular dead zone
			if (magnitude > XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)
			{
				mState.RX = 0.5f * (normalizedX + 1.0f) * INT8_MAX;
				mState.RY = 0.5f * (normalizedY + 1.0f) * INT8_MAX;
			}
			else //if the controller is in the deadzone zero out the magnitude
			{
				mState.RX = UINT8_MAX >> 1;
				mState.RY = UINT8_MAX >> 1;
			}
#pragma endregion

#pragma region CheckSum
			unsigned __int16 sum = 0;
			for (int i = 0; i < GAMEPAD_BYTES - 1; i++)
			{
				sum + mState._ARRAY[i];
			}
			mState.CS = static_cast<unsigned __int8>(sum & 0xFF);
#pragma endregion

#pragma endregion
		}
	}
}