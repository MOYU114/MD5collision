ihv = "0123456789abcdeffedcba9876543210"
out1 = "output1.bin"
out2 = "output2.bin"
IV = [0,0,0,0]
msg1block0, msg1block1, msg2block0, msg2block1 =[]

def find_collision(IV, msg1block0, msg1block1, msg2block0, msg2block1,flag):
    if flag:
		print("Generating first block: ")

	find_block0(msg1block0, IV)
	IHV= [IV[0], IV[1], IV[2], IV[3]]
	md5_compress(IHV, msg1block0)

	if flag:
		print("Generating second block: ")
	find_block1(msg1block1, IHV)

	for t in range (16):
		msg2block0[t] = msg1block0[t]
		msg2block1[t] = msg1block1[t]

	msg2block0[4] += 1 << 31; msg2block0[11] += 1 << 15; msg2block0[14] += 1 << 31
	msg2block1[4] += 1 << 31; msg2block1[11] -= 1 << 15; msg2block1[14] += 1 << 31
	if flag:
		print()
	return

def save_block(ofs, msg1block):


'''
for (int i = 0; i < 4; ++i):
    ss << hex << ihv.substr(i * 8, 8);
    ss >> IV[i];

msg1block0[16], msg1block1[16], msg2block0[16], msg2block1[16]
'''

find_collision(IV, msg1block0, msg1block1, msg2block0, msg2block1, True)
'''
ofstream ofs1(out1, ios::binary), ofs2(out2, ios::binary);
    if (!ofs1 || !ofs2) {
        cerr << "Error: cannot open output files." << endl;
        return 1;
    }
'''
save_block(ofs1, msg1block0)
save_block(ofs1, msg1block1)
save_block(ofs2, msg2block0)
save_block(ofs2, msg2block1)



