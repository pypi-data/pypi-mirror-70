"""
A Convolutional Encoding and Decoding

Copyright (c) March 2017, Mark Wickert
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
"""


"""
A forward error correcting coding (FEC) class which defines methods 
for performing convolutional encoding and decoding. Arbitrary 
polynomials are supported, but the rate is presently limited to r = 1/n,
where n = 2. Punctured (perforated) convolutional codes are also supported. 
The puncturing pattern (matrix) is arbitrary.

Two popular encoder polynomial sets are:

K = 3 ==> G1 = '111', G2 = '101' and 
K = 7 ==> G1 = '1011011', G2 = '1111001'.

A popular puncturing pattern to convert from rate 1/2 to rate 3/4 is
a G1 output puncture pattern of '110' and a G2 output puncture 
pattern of '101'.

Graphical display functions are included to allow the user to
better understand the operation of the Viterbi decoder.

Mark Wickert and Andrew Smit: October 2018.
"""
import numpy as np
from math import factorial
from fractions import Fraction
import matplotlib.pyplot as plt
import scipy.special as special
from sys import exit
import warnings
from sk_dsp_comm.digitalcom import Q_fctn
from sk_dsp_comm.fec_conv import trellis_nodes, trellis_branches, trellis_paths, binary, conv_Pb_bound, hard_Pk, soft_Pk
import rs_fec_conv

class fec_conv(object):
    """
    Class responsible for creating rate 1/2 convolutional code objects, and 
    then encoding and decoding the user code set in polynomials of G. Key
    methods provided include :func:`conv_encoder`, :func:`viterbi_decoder`, :func:`puncture`,
    :func:`depuncture`, :func:`trellis_plot`, and :func:`traceback_plot`.

    Parameters
    ----------
    G: A tuple of two binary strings corresponding to the encoder polynomials
    Depth: The decision depth employed by the Viterbi decoder method

    Returns
    -------
    

    Examples
    --------
    >>> from sk_dsp_comm import fec_conv
    >>> # Rate 1/2
    >>> cc1 = fec_conv.fec_conv(('101', '111'), Depth=10)  # decision depth is 10

    >>> # Rate 1/3
    >>> from sk_dsp_comm import fec_conv
    >>> cc2 = fec_conv.fec_conv(('101','011','111'), Depth=15)  # decision depth is 15

    
    """
    def __init__(self,G = ('111','101'), Depth = 10):
        """
        cc1 = fec_conv(G = ('111','101'), Depth = 10)
        Instantiate a Rate 1/2 or Rate 1/3 convolutional 
        coder/decoder object. Polys G1 and G2 are entered 
        as binary strings, e.g,
        
        Rate 1/2
        G1 = '111' and G2 = '101' for K = 3 and
        G1 = '1111001' and G2 = '1011011' for K = 7.

        Rate 1/3
        G1 = '111', G2 = '011' and G3 = '101' for K = 3 and
        G1 = '1111001', G2 = '1100101' and G3 = '1011011'
        for K= 7

        The rate will automatically be selected by the number
        of G polynomials (only rate 1/2 and 1/3 are available)

        Viterbi decoding has a decision depth of Depth.

        Data structures than manage the VA are created 
        upon instantiation via the __init__ method.

        Other ideal polynomial considerations (taken from
        "Introduction to Digital Communication" Second Edition
        by Ziemer and Peterson:
        
        Rate 1/2
        K=3 ('111','101')
        K=4 ('1111','1101')
        K=5 ('11101','10011')
        K=6 ('111101','101011')
        K=7 ('1111001','1011011')
        K=8 ('11111001','10100111')
        K=9 ('111101011','101110001')

        Rate 1/3
        K=3 ('111','111','101')
        K=4 ('1111','1101','1011')
        K=5 ('11111','11011','10101')
        K=6 ('111101','101011','100111')
        K=7 ('1111001','1100101','1011011')
        K=8 ('11110111','11011001','10010101')

        Mark Wickert and Andrew Smit October 2018
        """
        self.G_polys = G
        self.constraint_length = len(self.G_polys[0]) 
        self.Nstates = 2**(self.constraint_length-1) # number of states
        self.decision_depth = Depth
        self.input_zero = trellis_nodes(self.Nstates)
        self.input_one = trellis_nodes(self.Nstates)
        self.paths = trellis_paths(self.Nstates,self.decision_depth)
        self.rate = Fraction(1,len(G))
        
        if(len(G) == 2 or len(G) == 3):
            print('Rate %s Object' %(self.rate))
        else:
            print('Invalid rate. Use Rate 1/2 or 1/3 only')
            raise ValueError('Invalid rate. Use Rate 1/2 or 1/3 only')
            pass

        for m in range(self.Nstates):
            self.input_zero.fn[m] = m
            self.input_one.fn[m] = m
            # state labeling with LSB on right (more common)
            output0,state0 = self.conv_encoder([0],
                             binary(m,self.constraint_length-1))
            output1,state1 = self.conv_encoder([1],
                             binary(m,self.constraint_length-1))
            self.input_zero.tn[m] = int(state0,2)
            self.input_one.tn[m] = int(state1,2)
            if(self.rate == Fraction(1,2)):
                self.input_zero.out_bits[m] = 2*output0[0] + output0[1]
                self.input_one.out_bits[m] = 2*output1[0] + output1[1]
            elif(self.rate == Fraction(1,3)):
                self.input_zero.out_bits[m] = 4*output0[0] + 2*output0[1] + output0[2]
                self.input_one.out_bits[m] = 4*output1[0] + 2*output1[1] + output1[2]

        # Now organize the results into a branches_from structure that holds the
        # from state, the u2 u1 bit sequence in decimal form, and the input bit.
        # The index where this information is stored is the to state where survivors
        # are chosen from the two input branches.
        self.branches = trellis_branches(self.Nstates)

        for m in range(self.Nstates):
            match_zero_idx = np.where(self.input_zero.tn == m)
            match_one_idx = np.where(self.input_one.tn == m)
            if len(match_zero_idx[0]) != 0:
                self.branches.states1[m] = self.input_zero.fn[match_zero_idx[0][0]]
                self.branches.states2[m] = self.input_zero.fn[match_zero_idx[0][1]]
                self.branches.bits1[m] = self.input_zero.out_bits[match_zero_idx[0][0]]
                self.branches.bits2[m] = self.input_zero.out_bits[match_zero_idx[0][1]]
                self.branches.input1[m] = 0
                self.branches.input2[m] = 0
            elif len(match_one_idx[0]) != 0:
                self.branches.states1[m] = self.input_one.fn[match_one_idx[0][0]]
                self.branches.states2[m] = self.input_one.fn[match_one_idx[0][1]]
                self.branches.bits1[m] = self.input_one.out_bits[match_one_idx[0][0]]
                self.branches.bits2[m] = self.input_one.out_bits[match_one_idx[0][1]]
                self.branches.input1[m] = 1
                self.branches.input2[m] = 1
            else:
                print('branch calculation error')
                exit(1)
	
    def viterbi_decoder(self,x,metric_type='soft',quant_level=3):
        """
        A method which performs Viterbi decoding of noisy bit stream,
        taking as input soft bit values centered on +/-1 and returning 
        hard decision 0/1 bits.

        Parameters
        ----------
        x: Received noisy bit values centered on +/-1 at one sample per bit
        metric_type: 
            'hard' - Hard decision metric. Expects binary or 0/1 input values.
            'unquant' - unquantized soft decision decoding. Expects +/-1
                input values.
            'soft' - soft decision decoding.
        quant_level: The quantization level for soft decoding. Expected 
        input values between 0 and 2^quant_level-1. 0 represents the most 
        confident 0 and 2^quant_level-1 represents the most confident 1. 
        Only used for 'soft' metric type.

        Returns
        -------
        y: Decoded 0/1 bit stream

        Examples
        --------
        >>> import numpy as np
        >>> from numpy.random import randint
        >>> import rs_fec_conv.fec_conv as fec
        >>> import sk_dsp_comm.digitalcom as dc
        >>> import matplotlib.pyplot as plt
        >>> # Soft decision rate 1/2 simulation
        >>> N_bits_per_frame = 10000
        >>> EbN0 = 4
        >>> total_bit_errors = 0
        >>> total_bit_count = 0
        >>> cc1 = fec.fec_conv(('11101','10011'),25)
        >>> # Encode with shift register starting state of '0000'
        >>> state = '0000'
        >>> while total_bit_errors < 100:
        >>>     # Create 100000 random 0/1 bits
        >>>     x = randint(0,2,N_bits_per_frame)
        >>>     y,state = cc1.conv_encoder_rs(x,state)
        >>>     # Add channel noise to bits, include antipodal level shift to [-1,1]
        >>>     yn_soft = dc.cpx_AWGN(2*y-1,EbN0-3,1) # Channel SNR is 3 dB less for rate 1/2
        >>>     yn_hard = ((np.sign(yn_soft.real)+1)/2).astype(int)
        >>>     z = cc1.viterbi_decoder_rs(yn_hard,'hard')
        >>>     # Count bit errors
        >>>     bit_count, bit_errors = dc.bit_errors(x,z)
        >>>     total_bit_errors += bit_errors
        >>>     total_bit_count += bit_count
        >>>     print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                    (total_bit_count, total_bit_errors,\
                    total_bit_errors/total_bit_count))
        >>> print('*****************************************************')
        >>> print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                (total_bit_count, total_bit_errors,\
                total_bit_errors/total_bit_count))
        Rate 1/2 Object
        kmax =  0, taumax = 0
        Bits Received = 9976, Bit errors = 77, BEP = 7.72e-03
        kmax =  0, taumax = 0
        Bits Received = 19952, Bit errors = 175, BEP = 8.77e-03
        *****************************************************
        Bits Received = 19952, Bit errors = 175, BEP = 8.77e-03


        >>> # Consider the trellis traceback after the sim completes
        >>> cc1.traceback_plot()
        >>> plt.show()


        >>> # Compare a collection of simulation results with soft decision
        >>> # bounds
        >>> SNRdB = np.arange(0,12,.1)
        >>> Pb_uc = fec.conv_Pb_bound(1/3,7,[4, 12, 20, 72, 225],SNRdB,2)
        >>> Pb_s_third_3 = fec.conv_Pb_bound(1/3,8,[3, 0, 15],SNRdB,1)
        >>> Pb_s_third_4 = fec.conv_Pb_bound(1/3,10,[6, 0, 6, 0],SNRdB,1)
        >>> Pb_s_third_5 = fec.conv_Pb_bound(1/3,12,[12, 0, 12, 0, 56],SNRdB,1)
        >>> Pb_s_third_6 = fec.conv_Pb_bound(1/3,13,[1, 8, 26, 20, 19, 62],SNRdB,1)
        >>> Pb_s_third_7 = fec.conv_Pb_bound(1/3,14,[1, 0, 20, 0, 53, 0, 184],SNRdB,1)
        >>> Pb_s_third_8 = fec.conv_Pb_bound(1/3,16,[1, 0, 24, 0, 113, 0, 287, 0],SNRdB,1)
        >>> Pb_s_half = fec.conv_Pb_bound(1/2,7,[4, 12, 20, 72, 225],SNRdB,1)
        >>> plt.figure(figsize=(5,5))
        >>> plt.semilogy(SNRdB,Pb_uc)
        >>> plt.semilogy(SNRdB,Pb_s_third_3,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_4,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_5,'g')
        >>> plt.semilogy(SNRdB,Pb_s_third_6,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_7,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_8,'--')
        >>> plt.semilogy([0,1,2,3,4,5],[9.08e-02,2.73e-02,6.52e-03,\
                                8.94e-04,8.54e-05,5e-6],'gs')
        >>> plt.axis([0,12,1e-7,1e0])
        >>> plt.title(r'Soft Decision Rate 1/2 Coding Measurements')
        >>> plt.xlabel(r'$E_b/N_0$ (dB)')
        >>> plt.ylabel(r'Symbol Error Probability')
        >>> plt.legend(('Uncoded BPSK','R=1/3, K=3, Soft',\
                    'R=1/3, K=4, Soft','R=1/3, K=5, Soft',\
                    'R=1/3, K=6, Soft','R=1/3, K=7, Soft',\
                    'R=1/3, K=8, Soft','R=1/3, K=5, Sim', \
                    'Simulation'),loc='upper right')
        >>> plt.grid();
        >>> plt.show()


        >>> # Hard decision rate 1/3 simulation
        >>> N_bits_per_frame = 10000
        >>> EbN0 = 3
        >>> total_bit_errors = 0
        >>> total_bit_count = 0
        >>> cc2 = fec.fec_conv(('11111','11011','10101'),25)
        >>> # Encode with shift register starting state of '0000'
        >>> state = '0000'
        >>> while total_bit_errors < 100:
        >>>     # Create 100000 random 0/1 bits
        >>>     x = randint(0,2,N_bits_per_frame)
        >>>     y,state = cc2.conv_encoder(x,state)
        >>>     # Add channel noise to bits, include antipodal level shift to [-1,1]
        >>>     yn_soft = dc.cpx_AWGN(2*y-1,EbN0-10*np.log10(3),1) # Channel SNR is 10*log10(3) dB less
        >>>     yn_hard = ((np.sign(yn_soft.real)+1)/2).astype(int)
        >>>     z = cc2.viterbi_decoder(yn_hard.real,'hard')
        >>>     # Count bit errors
        >>>     bit_count, bit_errors = dc.bit_errors(x,z)
        >>>     total_bit_errors += bit_errors
        >>>     total_bit_count += bit_count
        >>>     print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                    (total_bit_count, total_bit_errors,\
                    total_bit_errors/total_bit_count))
        >>> print('*****************************************************')
        >>> print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                (total_bit_count, total_bit_errors,\
                total_bit_errors/total_bit_count))
        Rate 1/3 Object
        kmax =  0, taumax = 0
        Bits Received = 9976, Bit errors = 251, BEP = 2.52e-02
        *****************************************************
        Bits Received = 9976, Bit errors = 251, BEP = 2.52e-02


        >>> # Compare a collection of simulation results with hard decision
        >>> # bounds
        >>> SNRdB = np.arange(0,12,.1)
        >>> Pb_uc = fec.conv_Pb_bound(1/3,7,[4, 12, 20, 72, 225],SNRdB,2)
        >>> Pb_s_third_3_hard = fec.conv_Pb_bound(1/3,8,[3, 0, 15, 0, 58, 0, 201, 0],SNRdB,0)
        >>> Pb_s_third_5_hard = fec.conv_Pb_bound(1/3,12,[12, 0, 12, 0, 56, 0, 320, 0],SNRdB,0)
        >>> Pb_s_third_7_hard = fec.conv_Pb_bound(1/3,14,[1, 0, 20, 0, 53, 0, 184],SNRdB,0)
        >>> Pb_s_third_5_hard_sim = np.array([8.94e-04,1.11e-04,8.73e-06])
        >>> plt.figure(figsize=(5,5))
        >>> plt.semilogy(SNRdB,Pb_uc)
        >>> plt.semilogy(SNRdB,Pb_s_third_3_hard,'r--')
        >>> plt.semilogy(SNRdB,Pb_s_third_5_hard,'g--')
        >>> plt.semilogy(SNRdB,Pb_s_third_7_hard,'k--')
        >>> plt.semilogy(np.array([5,6,7]),Pb_s_third_5_hard_sim,'sg')
        >>> plt.axis([0,12,1e-7,1e0])
        >>> plt.title(r'Hard Decision Rate 1/3 Coding Measurements')
        >>> plt.xlabel(r'$E_b/N_0$ (dB)')
        >>> plt.ylabel(r'Symbol Error Probability')
        >>> plt.legend(('Uncoded BPSK','R=1/3, K=3, Hard',\
                    'R=1/3, K=5, Hard', 'R=1/3, K=7, Hard',\
                    ),loc='upper right')
        >>> plt.grid();
        >>> plt.show()

        >>> # Show the traceback for the rate 1/3 hard decision case
        >>> cc2.traceback_plot()
        """
        if metric_type == 'hard':
            # If hard decision must have 0/1 integers for input else float
            if np.issubdtype(x.dtype, np.integer):
                if x.max() > 1 or x.min() < 0:
                    raise ValueError('Integer bit values must be 0 or 1')
            else:
                raise ValueError('Decoder inputs must be integers on [0,1] for hard decisions')
        elif metric_type not in ['hard', 'soft', 'unquant']:
            print('Invalid metric type specified')
            raise ValueError('Invalid metric type specified. Use soft, hard, or unquant')

		# Format G into integer for Rust
        G = np.array([float(int(x, base=2)) for x in self.G_polys])
		
        # Call Rust Function
        y, paths_cum_metrics, paths_traceback_states, paths_traceback_bits = \
		    rs_fec_conv.viterbi_decoder(x.astype(float), metric_type, 
		    quant_level, G, self.decision_depth)
	
        # Convert lists to numpy arrays
        y = np.array(y)
        self.paths.cumulative_metric = np.array(paths_cum_metrics)
        self.paths.traceback_states = np.array(paths_traceback_states)
        self.paths.traceback_bits = np.array(paths_traceback_bits)
		
        # Update object fields
		
        return y

    def bm_calc(self,ref_code_bits, rec_code_bits, metric_type, quant_level):
        """
        distance = bm_calc(ref_code_bits, rec_code_bits, metric_type)
        Branch metrics calculation

        Mark Wickert and Andrew Smit October 2018
        """
        distance = 0
        if metric_type == 'soft': # squared distance metric
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(bits)):
                ref_bit = (2**quant_level-1)*int(bits[k],2)
                distance += (int(rec_code_bits[k]) - ref_bit)**2
        elif metric_type == 'hard': # hard decisions
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(rec_code_bits)):
                distance += abs(rec_code_bits[k] - int(bits[k]))
        elif metric_type == 'unquant': # unquantized
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(bits)):
                distance += (float(rec_code_bits[k])-float(bits[k]))**2
        else:
            print('Invalid metric type specified')
            raise ValueError('Invalid metric type specified. Use soft, hard, or unquant')
        return distance 

    def conv_encoder(self,input,state):
        """
        output, state = conv_encoder_rs(input,state)
        We get the 1/2 or 1/3 rate from self.rate
        Polys G1 and G2 are entered as binary strings, e.g,
        G1 = '111' and G2 = '101' for K = 3
        G1 = '1011011' and G2 = '1111001' for K = 7
        G3 is also included for rate 1/3
        Input state as a binary string of length K-1, e.g., '00' or '0000000' 
        e.g., state = '00' for K = 3
        e.g., state = '000000' for K = 7
        Mark Wickert and Andrew Smit 2018
        """
		
        # Format G into integer for Rust
        G = np.array([float(int(x, base=2)) for x in self.G_polys])
		
        # Call Rust Function
        if type(input) is list: 
            input = np.asarray(input)
        output, state = rs_fec_conv.conv_encoder(input.astype(float), state, G)
        output = np.array(output)
        
        return output, state

    def puncture(self,code_bits,puncture_pattern = ('110','101')):
        """
        Apply puncturing to the serial bits produced by convolutionally
        encoding.

        :param code_bits:
        :param puncture_pattern:
        :return:

        Examples
        --------
        This example uses the following puncture matrix:

        .. math::

           \\begin{align*}
               \\mathbf{A} = \\begin{bmatrix}
                1 & 1 & 0 \\\\
                1 & 0 & 1
                \\end{bmatrix}
           \\end{align*}

        The upper row operates on the outputs for the :math:`G_{1}` polynomial and the lower row operates on the outputs of
        the  :math:`G_{2}`  polynomial.

        >>> import numpy as np
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> cc = fec_conv(('101','111'))
        >>> x = np.array([0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
        >>> state = '00'
        >>> y, state = cc.conv_encoder(x, state)
        >>> cc.puncture(y, ('110','101'))
        array([ 0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  1.,  1.,  0.,  0.])
        """
        # Check to see that the length of code_bits is consistent with a rate
        # 1/2 code.
        L_pp = len(puncture_pattern[0])
        N_codewords = int(np.floor(len(code_bits)/float(2)))
        if 2*N_codewords != len(code_bits):
            warnings.warn('Number of code bits must be even!')
            warnings.warn('Truncating bits to be compatible.')
            code_bits = code_bits[:2*N_codewords]
        # Extract the G1 and G2 encoded bits from the serial stream.
        # Assume the stream is of the form [G1 G2 G1 G2 ...   ]
        x_G1 = code_bits.reshape(N_codewords,2).take([0],
                                 axis=1).reshape(1,N_codewords).flatten()
        x_G2 = code_bits.reshape(N_codewords,2).take([1],
                                 axis=1).reshape(1,N_codewords).flatten()
        # Check to see that the length of x_G1 and x_G2 is consistent with the
        # length of the puncture pattern
        N_punct_periods = int(np.floor(N_codewords/float(L_pp)))
        if L_pp*N_punct_periods != N_codewords:
            warnings.warn('Code bit length is not a multiple pp = %d!' % L_pp)
            warnings.warn('Truncating bits to be compatible.')
            x_G1 = x_G1[:L_pp*N_punct_periods]
            x_G2 = x_G2[:L_pp*N_punct_periods]
        #Puncture x_G1 and x_G1
        g1_pp1 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '1']
        g2_pp1 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '1']
        N_pp = len(g1_pp1)
        y_G1 = x_G1.reshape(N_punct_periods,L_pp).take(g1_pp1,
                            axis=1).reshape(N_pp*N_punct_periods,1)
        y_G2 = x_G2.reshape(N_punct_periods,L_pp).take(g2_pp1,
                            axis=1).reshape(N_pp*N_punct_periods,1)
        # Interleave y_G1 and y_G2 for modulation via a serial bit stream
        y = np.hstack((y_G1,y_G2)).reshape(1,2*N_pp*N_punct_periods).flatten()
        return y

    def depuncture(self,soft_bits,puncture_pattern = ('110','101'),
                   erase_value = 3.5):
        """
        Apply de-puncturing to the soft bits coming from the channel. Erasure bits
        are inserted to return the soft bit values back to a form that can be
        Viterbi decoded.

        :param soft_bits:
        :param puncture_pattern:
        :param erase_value:
        :return:

        Examples
        --------
        This example uses the following puncture matrix:

        .. math::

           \\begin{align*}
               \\mathbf{A} = \\begin{bmatrix}
                1 & 1 & 0 \\\\
                1 & 0 & 1
                \\end{bmatrix}
           \\end{align*}

        The upper row operates on the outputs for the :math:`G_{1}` polynomial and the lower row operates on the outputs of
        the  :math:`G_{2}`  polynomial.

        >>> import numpy as np
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> cc = fec_conv(('101','111'))
        >>> x = np.array([0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
        >>> state = '00'
        >>> y, state = cc.conv_encoder(x, state)
        >>> yp = cc.puncture(y, ('110','101'))
        >>> cc.depuncture(yp, ('110', '101'), 1)
        array([ 0., 0., 0., 1., 1., 1., 1., 0., 0., 1., 1., 0., 1., 1., 0., 1., 1., 0.]
        """
        # Check to see that the length of soft_bits is consistent with a rate
        # 1/2 code.
        L_pp = len(puncture_pattern[0])
        L_pp1 = len([g1 for g1 in puncture_pattern[0] if g1 == '1'])
        L_pp0 = len([g1 for g1 in puncture_pattern[0] if g1 == '0'])
        #L_pp0 = len([g1 for g1 in pp1 if g1 == '0'])
        N_softwords = int(np.floor(len(soft_bits)/float(2)))
        if 2*N_softwords != len(soft_bits):
            warnings.warn('Number of soft bits must be even!')
            warnings.warn('Truncating bits to be compatible.')
            soft_bits = soft_bits[:2*N_softwords]
        # Extract the G1p and G2p encoded bits from the serial stream.
        # Assume the stream is of the form [G1p G2p G1p G2p ...   ],
        # which for QPSK may be of the form [Ip Qp Ip Qp Ip Qp ...    ]
        x_G1 = soft_bits.reshape(N_softwords,2).take([0],
                                 axis=1).reshape(1,N_softwords).flatten()
        x_G2 = soft_bits.reshape(N_softwords,2).take([1],
                                 axis=1).reshape(1,N_softwords).flatten()
        # Check to see that the length of x_G1 and x_G2 is consistent with the
        # puncture length period of the soft bits
        N_punct_periods = int(np.floor(N_softwords/float(L_pp1)))
        if L_pp1*N_punct_periods != N_softwords:
            warnings.warn('Number of soft bits per puncture period is %d' % L_pp1)
            warnings.warn('The number of soft bits is not a multiple')
            warnings.warn('Truncating soft bits to be compatible.')
            x_G1 = x_G1[:L_pp1*N_punct_periods]
            x_G2 = x_G2[:L_pp1*N_punct_periods]
        x_G1 = x_G1.reshape(N_punct_periods,L_pp1)
        x_G2 = x_G2.reshape(N_punct_periods,L_pp1)
        #Depuncture x_G1 and x_G1
        g1_pp1 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '1']
        g1_pp0 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '0']
        g2_pp1 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '1']
        g2_pp0 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '0']
        x_E = erase_value*np.ones((N_punct_periods,L_pp0))
        y_G1 = np.hstack((x_G1,x_E))
        y_G2 = np.hstack((x_G2,x_E))
        [g1_pp1.append(val) for idx,val in enumerate(g1_pp0)]
        g1_comp = list(zip(g1_pp1,list(range(L_pp))))
        g1_comp.sort()
        G1_col_permute = [g1_comp[idx][1] for idx in range(L_pp)]
        [g2_pp1.append(val) for idx,val in enumerate(g2_pp0)]
        g2_comp = list(zip(g2_pp1,list(range(L_pp))))
        g2_comp.sort()
        G2_col_permute = [g2_comp[idx][1] for idx in range(L_pp)]
        #permute columns to place erasure bits in the correct position
        y = np.hstack((y_G1[:,G1_col_permute].reshape(L_pp*N_punct_periods,1),
                       y_G2[:,G2_col_permute].reshape(L_pp*N_punct_periods,
                       1))).reshape(1,2*L_pp*N_punct_periods).flatten()
        return y

    def trellis_plot(self,fsize=(6,4)):
        """
        Plots a trellis diagram of the possible state transitions.

        Parameters
        ----------
        fsize : Plot size for matplotlib.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> cc = fec_conv()
        >>> cc.trellis_plot()
        >>> plt.show()
        """

        branches_from = self.branches
        plt.figure(figsize=fsize)

        plt.plot(0,0,'.')
        plt.axis([-0.01, 1.01, -(self.Nstates-1)-0.05, 0.05])
        for m in range(self.Nstates):
            if branches_from.input1[m] == 0:
                plt.plot([0, 1],[-branches_from.states1[m], -m],'b')
                plt.plot([0, 1],[-branches_from.states1[m], -m],'r.')
            if branches_from.input2[m] == 0:
                plt.plot([0, 1],[-branches_from.states2[m], -m],'b')
                plt.plot([0, 1],[-branches_from.states2[m], -m],'r.')
            if branches_from.input1[m] == 1:
                plt.plot([0, 1],[-branches_from.states1[m], -m],'g')
                plt.plot([0, 1],[-branches_from.states1[m], -m],'r.')
            if branches_from.input2[m] == 1:
                plt.plot([0, 1],[-branches_from.states2[m], -m],'g')
                plt.plot([0, 1],[-branches_from.states2[m], -m],'r.')
        #plt.grid()
        plt.xlabel('One Symbol Transition')
        plt.ylabel('-State Index')
        msg = 'Rate %s, K = %d Trellis' %(self.rate, int(np.ceil(np.log2(self.Nstates)+1)))
        plt.title(msg)

    def traceback_plot(self,fsize=(6,4)):
        """
        Plots a path of the possible last 4 states.

        Parameters
        ----------
        fsize : Plot size for matplotlib.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> from sk_dsp_comm import digitalcom as dc
        >>> import numpy as np
        >>> cc = fec_conv()
        >>> x = np.random.randint(0,2,100)
        >>> state = '00'
        >>> y,state = cc.conv_encoder(x,state)
        >>> # Add channel noise to bits translated to +1/-1
        >>> yn = dc.cpx_AWGN(2*y-1,5,1) # SNR = 5 dB
        >>> # Translate noisy +1/-1 bits to soft values on [0,7]
        >>> yn = (yn.real+1)/2*7
        >>> z = cc.viterbi_decoder(yn)
        >>> cc.traceback_plot()
        >>> plt.show()
        """
        traceback_states = self.paths.traceback_states
        plt.figure(figsize=fsize)
        plt.axis([-self.decision_depth+1, 0, 
                  -(self.Nstates-1)-0.5, 0.5])
        M,N = traceback_states.shape
        traceback_states = -traceback_states[:,::-1]

        plt.plot(range(-(N-1),0+1),traceback_states.T)
        plt.xlabel('Traceback Symbol Periods')
        plt.ylabel('State Index $0$ to -$2^{(K-1)}$')
        plt.title('Survivor Paths Traced Back From All %d States' % self.Nstates)
        plt.grid()
