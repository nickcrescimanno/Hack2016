#include "nout.h"

#define BUFLEN 512


namespace Hack2016
{
	nout::nout(char const * server_name, unsigned __int16 const port)
	{
		pBuff = reinterpret_cast<char *>(malloc(MAX_BUFFSIZE));

		int slen = sizeof(si_other);
		WSADATA wsa;

		//Initialise winsock
		printf("\nInitialising Winsock...");
		if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		{
			printf("Failed. Error Code : %d", WSAGetLastError());
			exit(EXIT_FAILURE);
		}
		printf("Initialised.\n");

		//create socket
		if ((cSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR)
		{
			printf("socket() failed with error code : %d", WSAGetLastError());
			exit(EXIT_FAILURE);
		}

		//setup address structure
		memset((char *)&si_other, 0, sizeof(si_other));
		si_other.sin_family = AF_INET;
		si_other.sin_port = htons(port);
		si_other.sin_addr.S_un.S_addr = inet_addr(server_name);
	}

	nout::~nout(void)
	{
		// Kill socket
		if (SOCKET_ERROR != cSocket) {
			closesocket(cSocket);
		}

		WSACleanup();

		free(pBuff);
	}

	bool nout::Transmit(void)
	{
		if (SOCKET_ERROR == cSocket) {
			return false;
		}

		if (sendto(cSocket, pBuff, buffSize, 0, (struct sockaddr *) &si_other, sizeof(sockaddr_in)) == SOCKET_ERROR)
		{
			printf("sendto() failed with error code : %d", WSAGetLastError());
			return false;
		}

		return true;
	}

	bool nout::SetBuffer(const char * const pData, const size_t dataSize)
	{
		if (dataSize > MAX_BUFFSIZE) {
			return false;
		}

		memcpy(pBuff, pData, dataSize);
		buffSize = dataSize;
	}
}