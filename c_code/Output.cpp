#include "Output.h"

namespace Hack2016
{
	Output::Output()
	{
		pSignal = new nout("127.0.0.1", 4444);
		pGamepad = new Gamepad(0);
	}


	Output::~Output()
	{
		if (pSignal)
			delete pSignal;
		pSignal = nullptr;

		if (pGamepad)
			delete pGamepad;
		pGamepad= nullptr;

		Stop();	
	}

	void Output::Update()
	{
		pGamepad->Update();
		if (pGamepad->GetState()._RAW == oldState._RAW)
			return;

		oldState._RAW = pGamepad->GetState()._RAW;

		pSignal->SetBuffer(reinterpret_cast<char *>(&oldState), sizeof(GamepadState));
	}

	void OutputLoop(Output * pOut)
	{
		// Update Gamepad
		while (true)
		{
			pOut->Update();
			Sleep(GAMEPAD_SLEEP);
		}
	}

	void Output::Run()
	{
		pThread = new std::thread(&OutputLoop, this);
	}

	void Output::Stop()
	{
		if (pThread){
			pThread->join();
			delete pThread;
			pThread = nullptr;
		}
	}
}