'''
	@ Author : Hotae Lee
	@ Date : 05/25/2020
	@ Function : (1)Import log file and classify the trajectories according to ID (2) Save when collisions occur and what collides 			
					--> logging_trajectory(filename)			
	@ Parameters : 
	@ Variables : 
	@ Retruns :  traj_list[k](np array), collision(list), trace_time(list), n_obj(int), bool_success(bool), ID_list(list)
	@ Description : 
	@ TODO : 
'''

import numpy as np

'''
-----------------------------------------------------------------------------------
Import json files and parse all objects
-----------------------------------------------------------------------------------
'''


# Change the log file to the matrix/vector form

'''
From the log file, we have to get t-vector, state-vector [vx,vy,v_ang,x,y,rotation] of each object
Those objects would be only a ball or wood blocks. It's not necessary to get other things' trajectory since they are stationary. 
e.g. traj1 = N by 7 matrix = [time(1:N).T, state with 6 elements(1:N).T] (traj1 is for each ID)

Thus, after this code runs, we can have n_obj matrices like traj_list[k] corresponding to traj_bal, traj_block1, traj_block2,...
'''
def logging_trajectory(filename):		
	with open('{}.log'.format(filename),'rt') as f:
		content = f.readlines()

	print(type(content)) # list
	print(content[0]) #string

	# The number of log lines
	n_log = len(content)

	# Change each string into a list (split it by the whitespace)
	for k in range(n_log):
		content[k] = content[k].split() # content[k] = [5875.626	trace	YT6C	168	-11	0	176	204	0]

	# Split  "trace" case and "collisionStart, collisionEnd"
	trace = []
	collision = []
	bool_success = False
	for k in range(n_log):
		if content[k][1] == "trace":
			# change string to float for time and states
			for j in [0,3,4,5,6,7,8]:
				content[k][j] = float(content[k][j])
			trace.append(content[k])
		elif content[k][1] == "collisionStart" or content[k][1] == "collisionEnd":		
			# change string to float for time only
			content[k][0] = float(content[k][0])
			collision.append(content[k]) # [time, collision type, objA objB]
		elif content[k][1] == "levelComplete":
			bool_success = True
		else:
			pass
			

	n_trace = len(trace)
	n_collision = len(collision)

	# Initialize matrices
	trace_time = []

	# Check how many types of objects there are
	n_obj = 1
	count_flag = False
	loop_flag = True
	k = 1
	testID = trace[0][2]
	ID_list = []
	ID_list.append(testID)

	while loop_flag == True:
		temp = trace[k]
		if temp[2] == testID:
			loop_flag = False
		else:
			n_obj = n_obj + 1
			ID_list.append(temp[2])
		k = k+1

	'''
	while loop_flag == True:
		temp = trace[k]
		if count_flag == False:
			# print(temp[1])
			if temp[1] == "trace": # first time to meet 'trace'
				trace_start = k + 1
				count_flag = True
				testID = content[k][2] # allocate testID
				print(testID)			
		else:
			if temp[2] == testID: # check when testID is different from ID		
				loop_flag = False
			else:
				print(temp[2])
				n_obj = n_obj + 1	
		k = k + 1
	'''

	# make the object's list
	'''
	traj_list[k] = N by 6 matrix (np.array)
	trace_time = N by 1 matrix (list)
	'''

	traj_list = []
	for k in range(n_obj):
		traj_list.append([])

	# sort by ID
	for k in range(0,n_trace,n_obj):
		for i in range(n_obj):
			temp = trace[k+i]
			if temp[1] == "trace":
				traj_list[i].append(temp[3:9])	
		trace_time.append(float(trace[k][0])) # save time as a float (unit : ms)
	# Change the list into the np array
	for k in range(n_obj):
		traj_list[k] = np.array(traj_list[k])
			
	return 	traj_list, trace_time, collision, n_obj, bool_success, ID_list


if __name__ == "__main__":
	traj_list, trace_time, collision, n_obj, bool_success, ID_list = logging_trajectory("bb")		
	print("ID list is {}".format(ID_list))	
	print("The number of time log is {}".format(len(trace_time)))
	print("The collision list has an element like {}".format(collision[4]))
	print(type(collision[4][0]))
	print("The trace time is {}".format(trace_time[1]))
	print("The traj_list[0] has an element like {}".format(traj_list[0][2]))
	print(traj_list[0].shape)

