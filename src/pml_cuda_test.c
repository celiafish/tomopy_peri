/*
    Copyright 2014-2015 Dake Feng, Peri LLC, dakefeng@gmail.com

    This file is part of TomograPeri.

    TomograPeri is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TomograPeri is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TomograPeri.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "pml_cuda.h"
#include <stdio.h>

int main()
{
	if (test_cuda()==PERI_CALL_SUCCESS)
	{
		printf("test Cuda successed!\n");
		return 0;
	}
	printf("test Cuda failed..\n");
	return 1;
}
