#!/usr/bin/env bash

# to sed: {_{_{BACKEND_URL}_}_}
# to sed: {_{_{RANDOM_SEQ}_}_}
# to sed: {_{_{RANDOM_STRING_SEQ}_}_}

numbers=(); for i in {1..7}; do numbers+=($(( (RANDOM % 5) + 1 ))); done; joined_numbers=$(IFS=, ; echo "${numbers[*]}"); 

echo "BACKEND_URL: '$BACKEND_URL'"
echo "RANDOM_SEQ: '$joined_numbers'"
echo "RANDOM_STRING_SEQ: '$RANDOM_STRING_SEQ'"

sed -i'' -e "s|{_{_{BACKEND_URL}_}_}|$BACKEND_URL|" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt
sed -i'' -e "s|{_{_{RANDOM_SEQ}_}_}|$joined_numbers|" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt
sed -i'' -e "s|{_{_{RANDOM_STRING_SEQ}_}_}|$RANDOM_STRING_SEQ|" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt

grep -A 1 "val retrofit = Retrofit.Builder()" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt
grep "val correctSequence = listOf" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt
grep -B 2 -A 2 "fun callSecret(): Call<Message>" app/src/main/java/com/kksctf/ostrovok24/MainActivity.kt

./gradlew build

echo "Building done"

RESULT="./app/build/outputs/apk/debug/app-debug.apk"

ls -la "$RESULT"
cp "$RESULT" $EXPORT_PATH/build.apk

echo "Done!"
