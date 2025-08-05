---
categories:
    - Tools
---
# Convert Gif(or MP4) To Telegram Sticker

## Requirements

These are the requirements Telegram has given for the video stickers:

1. Video must be in .WEBM format, up to 30 FPS.
2. Video must be encoded with the VP9 codec.
3. Video must have no audio stream.
4. For stickers, one side must be 512 pixels in size – the other side can be 512 pixels or less.
5. Duration must not exceed 3 seconds.
6. Video should be looped for optimal user experience.
7. Video size should not exceed 256 KB after encoding.

## FFMPEG parameters to follow there requirements

1. .WEBM format `output.webm`, up to 30 FPS `-filter:v fps=30`
2. Encoded with the VP9 codec `-c:v libvpx-vp9`
3. No audio stream `-an`
4. One side must be 512 pixels in size – the other side can be 512 pixels or less `-vf 'scale=512:512:force_original_aspect_ratio=decrease`(Check the end result and tweak this value if the aspect ratio is wrong or ffmpeg cuts something you don't want)
5. Duration must not exceed 3 seconds `-ss 00:00:00 -t 00:00:03` (You can change -ss to the specific time in video you want to start capture. -t is capture length so you can change it to capture shorter parts but it shouldn't exceed 3 seconds)
6. Video should be looped `-stream_loop -1` (-1 means infinite loop)
7. Video size should not exceed 256 KB after encoding `-b:v 512k`. This is entirely depended on the source video and you may have to change this value to lower if the file size is too big.

## Examples

### Convert one video to Telegram format

```bash
#!/bin/bash
ffmpeg -ss 00:00:00 -t 00:00:03 -stream_loop -1 -i input.mp4 -c:v libvpx-vp9 -filter:v fps=30 -b:v 512k -an -vf 'scale=512:512:force_original_aspect_ratio=decrease' output.webm
```

### Convert entire folder of videos to Telegram format while making sure each file have correct file size

```bash
#!/bin/bash

# stat uses different flag on Linux and macOS
if stat --version >/dev/null 2>&1; then
    # GNU stat (Linux)
    stat_command='stat -c%s'
else
    # BSD stat (macOS)
    stat_command='stat -f%z'
fi

for file in *.mp4 *.gif; do
    # Skip if no files match
    [ -e "$file" ] || continue

    # Get filename without extension
    base="${file%.*}"
    out="out/${base}.webm"

    # Initial bitrate
    bitrate=512k

    # Convert to webm with Telegram sticker requirements
    ffmpeg -y -ss 00:00:00 -t 00:00:03 -stream_loop -1 -i "$file" \
        -c:v libvpx-vp9 -filter:v fps=30 -b:v $bitrate -an \
        -vf 'scale=512:512:force_original_aspect_ratio=decrease' "$out"

    # Check file size and reduce bitrate if needed
    max_size=262144  # 256 KB in bytes
    tries=0
    while [ $($stat_command "$out") -gt $max_size ] && [ $tries -lt 5 ]; do
        # Reduce bitrate by 20%
        bitrate=$(echo "$bitrate" | awk -F'k' '{printf "%dk", int($1*0.8)}')
        echo "File $out is too big, reducing bitrate to $bitrate and re-encoding..."
        ffmpeg -y -ss 00:00:00 -t 00:00:03 -stream_loop -1 -i "$file" \
            -c:v libvpx-vp9 -filter:v fps=30 -b:v $bitrate -an \
            -vf 'scale=512:512:force_original_aspect_ratio=decrease' "$out"
        tries=$((tries+1))
    done

    if [ $($stat_command "$out") -le $max_size ]; then
        echo "Converted $file -> $out (size: $($stat_command "$out") bytes)"
    else
        echo "Warning: $out is still larger than 256 KB after $tries attempts."
    fi
done
```
