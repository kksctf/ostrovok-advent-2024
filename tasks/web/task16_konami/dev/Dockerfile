# docker run --rm -v "$HOME/.dockercache/gradle":"/root/.gradle" -v ./build:/project mingc/android-build-box bash -c 'cd /project; ./gradlew build'

FROM mingc/android-build-box

WORKDIR /project

COPY ./build /project

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
