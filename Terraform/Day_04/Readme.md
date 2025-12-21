# Important points to remember / state file / remote backend

# 1. store state file to remote backend
# 2. Do not update / delete the file
# 3. state locking
# 4. isolation of statefile
# 5. Remote backend

# we will create s3 bucket as remote backend to store our statefile and keep it secure. so
# In our counfiguration and inside terraform block we will be keeping backend configuration. There is desired state and there is actual state in terraform statefile...that means whenever we are creating the infrastructure at that time terraform statefile will compare actual state and the desired state. Lets say when you are creating the infrastructure for the first time such as (s3 bucket, vpc, ec2 instance) then at that time our desired state state will be these three resources and our actual state would be nothing so it will create this three resources. if lets say three resources are there in infrastructure and in desired state we are having two resources and if we run terraform apply then it will compare with actual state and then it will create the two resources in infrastructure..one resource will be removed.


