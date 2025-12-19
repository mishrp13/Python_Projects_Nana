
# Just the Normal installation

# we need Terraform to create our infrastructure in Aws or in any cloud provider.
# Let's say there are multiple environments for our application and the applications are tier 3 application
# (user facing,Backend,database) --> tier 3...Then it become really combersome to create the infrastructure and mangae the infrastructure one by one.
# There might be scenarios where our application may run in multiple platforms so we need to to create the 
# the infrastructure with the help of Terraform !!
# we can have CICD pipleline in place in our github repository so that whenever the files changes or we do any changes in our terraform files then it triggres the pipeline and creates the infrastructure for us! we can manage the state changes of our terraform file. we can also do the drift detection in Terraform. For destorying the  infrasturce such as staging environment or performance testing enviornment if they are not in use . we can simply use "" Terraform Destory "

