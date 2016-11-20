#pragma once

#define WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <stdlib.h>
#include <stdio.h>

// Need to link with Ws2_32.lib, Mswsock.lib, and Advapi32.lib
#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

#define MAX_BUFFSIZE	512
#define DEFAULT_PORT	"4444" // "27015"

namespace Hack2016
{
	class nout
	{
	private:
		char * pBuff;
		size_t buffSize;

		SOCKET	cSocket;

		struct sockaddr_in si_other;

	public:
		nout(char const *, unsigned __int16 const);
		~nout(void);

		bool SetBuffer(const char * const, const size_t);
		bool Transmit(void);
	};
}
