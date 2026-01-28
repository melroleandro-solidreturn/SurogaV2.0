# IMPORTANT NOTE: Ensure the port number configured here matches the one expected by the Suroga API library (Suroo lib).
# The port exposed by the docker container must align with the one designated within Suroga codebase configurations
# to ensure proper networking. Any discrepancy can lead to connectivity issues where the API consumers, including the
# Suroga API library, may be unable to reach the exposed services, resulting in operational failures. Consistency in port
# configuration is critical for seamless integration and reliable service availability.


# It's using an official Python image, version 3.9, from Docker Hub. The Python image already has Python installed and configured.
FROM python:3.10

# Linux command to update the list of available packages. After the update, we're clearing out the package list to reduce the size of our image. It's a good practice to remove unnecessary files to keep Docker images small.
RUN apt-get update \
	&& rm -rf /var/lib/apt/lists/* 

# Sets the working directory for any instructions that follow in the Dockerfile. It's similar to cd /usr/src/app. If the directory does not exist, Docker will create it.
WORKDIR /usr/src/app
#Copies the requirements.txt file from your host machine into the container's working directory. The requirements.txt file lists all the Python packages your application needs.
COPY requirements.txt ./

# Installs the Python packages specified in requirements.txt. This is a separate step from copying requirements.txt so Docker can cache the installed packages. It won't need to re-install them every time you make changes to your codebase, as long as requirements.txt doesn't change.
RUN pip install -r requirements.txt

#Copies the rest of your application code into the container's working directory.
COPY . .

#Tells Docker that the container will listen on port 8000 at runtime. EXPOSE does not publish the port itself; it acts more like documentation between the person who builds the image and the person who runs the container.
EXPOSE 8000

#Specifies the command to run when the container starts. In this case, it's starting the Django development server on port 8000 and binding it to all network interfaces inside the container with 0.0.0.0:8000.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
