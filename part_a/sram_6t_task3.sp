* AMCAS Task 3: VDD Sweep
.include 45nm_bulk.txt
.param VDD=1.1 VBL=1.1

Vdd vdd 0 'VDD'
Vwl wl 0 PWL (0 0 1n 0 1.05n 'VDD')

* Baseline transistor sizing restored
MP1 qb q vdd vdd pmos W=0.15u L=0.045u
MN1 qb q 0 0 nmos W=0.20u L=0.045u
MP2 q qb vdd vdd pmos W=0.15u L=0.045u
MN2 q qb 0 0 nmos W=0.20u L=0.045u

MA1 bl wl q 0 nmos W=0.16u L=0.045u
MA2 blb wl qb 0 nmos W=0.16u L=0.045u

Cbl bl 0 180f IC='VBL'
Cblb blb 0 180f IC='VBL'

.ic v(q)=0 v(qb)='VDD'

.control
let v_current = 1.1
let vdd_stop = 0.59
let vdd_step = -0.05

* Create the output file with headers
echo "vdd dv" > task3_sweep.txt

while v_current >= vdd_stop
    alterparam VDD = $&v_current
    alterparam VBL = $&v_current
    reset
    
    tran 5p 4n uic
    let current_dv = v(blb) - v(bl)
    meas tran tmp_dv FIND current_dv AT=2.0n
    
    * Append the scalar values directly to the file
    echo $&v_current $&tmp_dv >> task3_sweep.txt
    
    let v_current = v_current + vdd_step
end
.endc
.end