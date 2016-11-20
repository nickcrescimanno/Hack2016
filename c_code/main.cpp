#include <thread>
#include <iostream>
#include "Gamepad.h"
#include "Output.h"

#include "nout.h"

#include "package.h"

#define LOCAL_IP "127.0.0.1"
#define PI_IP "173.116.176.240"
#define S_IP "164.107.133.86"
#define A_IP "34.192.185.121"
#define PORT 3333

int main(int argc, char* argv[])
{
	using namespace Hack2016;

	Gamepad g(0);
	nout udp(A_IP, PORT);

	// Test Gamepad
	while (true)
	{
		// Clear stream
		system("cls");

		Package p = Package::FromGamepadState(g.GetState());

		g.Update();
		std::cout << p._RAW;

		// char * pTest = "cat";
		// udp.SetBuffer(pTest, 4);
		udp.SetBuffer(reinterpret_cast<const char *>(&p), sizeof(Package));
		udp.Transmit();

		Sleep(10);
	}

	return 0;
}

