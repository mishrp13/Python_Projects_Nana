"This Jenkins pipeline automates the build, test, code quality analysis, containerization, and deployment of a Java application to AWS ECS.

It starts by fetching the code from GitHub. Then it builds the application using Maven and archives the .war artifact for reference. Next, it runs unit tests to validate the code logic and performs a Checkstyle analysis to ensure the code follows proper formatting and naming conventions.

After that, the pipeline runs SonarQube analysis to detect bugs, vulnerabilities, and code smells, followed by a Quality Gate check that stops the pipeline if the code doesn’t meet quality standards.

Once the code passes all checks, the pipeline builds a Docker image, tags it, and pushes it to AWS ECR. Local Docker images are cleaned up to save space. Finally, it deploys the application to AWS ECS by forcing a new service deployment with the latest image.

Overall, it’s a full CI/CD workflow ensuring automated builds, quality checks, containerization, and deployment—all in a single pipeline."