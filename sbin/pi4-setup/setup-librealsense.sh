


# enlarge the swap file for building
sudo cp sbin/files/etc/dphys-swapfile /etc
sudo /etc/init.d/dphys-swapfile restart swapon -s

git clone https://github.com/IntelRealSense/librealsense.git

cd librealsense/
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger

mkdir build && cd build

# 32 bit
# cmake \
# -DCMAKE_BUILD_TYPE=RELEASE \
# -DBUILD_SHARED_LIBS=false \
# -DBUILD_PYTHON_BINDINGS=true \
# -DPYTHON_INCLUDE_DIR=/usr/include/python3.9 \
# -DPYTHON_EXECUTABLE=/usr/bin/python3.9 \
# -DPYTHON_LIBRARY=/usr/lib/python3.9/config-3.9-arm-linux-gnueabihf/libpython3.9.so \
# ..

# 64 bit
cmake \
-DCMAKE_BUILD_TYPE=RELEASE \
-DBUILD_SHARED_LIBS=false \
-DBUILD_PYTHON_BINDINGS=true \
-DPYTHON_INCLUDE_DIR=/usr/include/python3.9 \
-DPYTHON_EXECUTABLE=/usr/bin/python3 \
-DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.9.so \
..

make
sudo make install
