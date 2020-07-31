Steps for Setting Up a New PI
-----------------------------

1. raspi-config
   - boot to Console
   - enable SSH

2. Set up static IP on the router

3. Mount /tmp and /var/log in ramdisk to avoid wear on the sd card. 
   Add these to /etc/fstab

   tmpfs           /var/log        tmpfs   defaults,nosuid,mode=0755,nodev,noatime 0       0
   tmpfs           /tmp    tmpfs   defaults,nosuid,mode=0755,nodev,noatime 0       0

4. Disable SWAP file - though seems to already be off on the 3B+?
   sudo dphys-swapfile swapoff   
