import numpy as np
import matplotlib.pyplot as plt

seismic_data = np.fromfile('data/xs.dat', dtype=np.float32).reshape(128, 128, 128)
fault_data = np.fromfile('data/gt.dat', dtype=np.float32).reshape(128, 128, 128)
pred = np.fromfile('data/ep.dat', dtype=np.float32).reshape(128, 128, 128)
# apply sigmoid and threshold
pred = 1 / (1 + np.exp(-pred))
pred = (pred > 0.5).astype(np.float32)
osv = np.fromfile('data/fv.dat', dtype='>f4').reshape(128, 128, 128)
osv_thin = np.fromfile('data/fvt.dat', dtype='>f4').reshape(128, 128, 128)

# Plotting
fig = plt.figure(figsize=(20,20))

# Time slice
k1 = 50
plt.subplot(3, 5, 1)
plt.imshow(seismic_data[k1,:,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Input - Time Slice')
plt.subplot(3, 5, 2)
plt.imshow(pred[k1,:,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Prediction')
plt.subplot(3, 5, 3)
plt.imshow(osv[k1,:,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV')
plt.subplot(3, 5, 4)
plt.imshow(osv_thin[k1,:,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV Thin')
plt.subplot(3, 5, 5)
plt.imshow(fault_data[k1,:,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('GT - Time Slice')

# Inline slice
k2 = 110
plt.subplot(3, 5, 6)
plt.imshow(seismic_data[:,k2,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Input - Inline Slice')
plt.subplot(3, 5, 7)
plt.imshow(pred[:,k2,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Prediction')
plt.subplot(3, 5, 8)
plt.imshow(osv[:,k2,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV')
plt.subplot(3, 5, 9)
plt.imshow(osv_thin[:,k2,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV Thin')
plt.subplot(3, 5, 10)
plt.imshow(fault_data[:,k2,:], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('GT - Inline Slice')

# Xline slice
k3 = 10
plt.subplot(3, 5, 11)
plt.imshow(seismic_data[:,:,k3], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Input - Xline Slice')
plt.subplot(3, 5, 12)
plt.imshow(pred[:,:,k3], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('Prediction')
plt.subplot(3, 5, 13)
plt.imshow(osv[:,:,k3], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV')
plt.subplot(3, 5, 14)
plt.imshow(osv_thin[:,:,k3], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('OSV thin')
plt.subplot(3, 5, 15)
plt.imshow(fault_data[:,:,k3], cmap=plt.cm.bone, interpolation='nearest', aspect=1)
plt.title('GT - Xline Slice')

plt.show()