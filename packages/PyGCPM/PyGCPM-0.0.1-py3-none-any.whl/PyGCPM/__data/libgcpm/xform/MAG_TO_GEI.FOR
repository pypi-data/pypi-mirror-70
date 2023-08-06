c
c	transformation from MAG to GEI coordinates
c
c	itime(1)=yyyyddd		year (yyyy) and day-of-year (ddd)
c	itime(2)=msec		miliseconds of day in UT
c	coordinates x_in and x_out are Cartesian and real*4
c
	subroutine MAG_to_gei (itime,x_in,x_out)
c
	real*4 x_in(3),x_out(3),temp1(3)
	integer*4 itime(2)
c
	call t5(itime,x_in,temp1,-1)
	call t1(itime,temp1,x_out,-1)
c
	return
	end

