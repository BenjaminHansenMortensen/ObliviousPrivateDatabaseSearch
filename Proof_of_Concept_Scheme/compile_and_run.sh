#!/bin/bash

cp MP_SPDZ_Scripts/MP_SPDZ_Only_Scheme.mpc ../../MP-SPDZ/Programs/Source/MP_SPDZ_Only_Scheme.mpc

cd ../../MP-SPDZ/

./compile.py MP_SPDZ_Only_Scheme

./atlas-party.x MP_SPDZ_Only_Scheme -p 0 -N 3 -IF ../PycharmProjects/MasterThesis/Client/MP_SPDZ_Inputs/MP_SPDZ_Only_Input -OF ../PycharmProjects/MasterThesis/Client/MPSPDZ_Outputs/MP_SPDZ_Only_Output &
./atlas-party.x MP_SPDZ_Only_Scheme -p 1 -N 3 -IF ../PycharmProjects/MasterThesis/Server/MP_SPDZ_Inputs/MP_SPDZ_Only_Input &
./atlas-party.x MP_SPDZ_Only_Scheme -p 2 -N 3