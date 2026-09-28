#!/usr/bin/env python3
"""Apply the v8.2 UI/editor update to the current android_project.py.

This patch is intentionally kept separate from the generated Android project so the
existing v8.1 generator remains the single source of truth. GitHub Actions can run
this file immediately before android_project.py.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, found {count}")
    return text.replace(old, new, 1)


def insert_after(text: str, marker: str, addition: str, label: str) -> str:
    count = text.count(marker)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 marker, found {count}")
    return text.replace(marker, marker + addition, 1)


def replace_section(text: str, start: str, end: str, replacement: str, label: str) -> str:
    start_at = text.find(start)
    if start_at < 0:
        raise RuntimeError(f"{label}: start marker not found")
    end_at = text.find(end, start_at)
    if end_at < 0:
        raise RuntimeError(f"{label}: end marker not found")
    end_at += len(end)
    return text[:start_at] + replacement + text[end_at:]


def apply_patch(source: str) -> str:
    text = source

    # App version for this update.
    text = replace_once(text, "        versionCode 20", "        versionCode 21", "versionCode")
    text = replace_once(text, "        versionName '8.1'", "        versionName '8.2'", "versionName")

    # ------------------------------------------------------------------
    # 1) Timeline: deleted ranges are physically collapsed in the UI.
    #    Public positions remain source-time positions, so export semantics
    #    and undo/redo stay compatible with the existing editor model.
    # ------------------------------------------------------------------
    text = replace_once(
        text,
        "/** Compact editor timeline that shows the playhead, split points, deleted ranges and reversed ranges. */",
        "/** Compact editor timeline. Deleted ranges collapse out of the bar like a gallery editor. */",
        "timeline comment",
    )

    text = replace_once(
        text,
        '''    void setRanges(List<AnimationEdits.TimeRange> deleted,\n                   List<AnimationEdits.TimeRange> reversed) {\n        deletedRanges = deleted == null ? Collections.emptyList() : deleted;\n        reversedRanges = reversed == null ? Collections.emptyList() : reversed;\n        invalidate();\n    }''',
        '''    void setRanges(List<AnimationEdits.TimeRange> deleted,\n                   List<AnimationEdits.TimeRange> reversed) {\n        // Normalize ranges once here. The deleted pieces are not painted: they are removed\n        // from the visible time axis, while callers can continue using absolute source time.\n        AnimationEdits normalized = new AnimationEdits(\n                0, 0, 1.0, AnimationEdits.CROP_NONE, 0, false, false,\n                0, 100, 100,\n                deleted == null ? Collections.emptyList() : deleted,\n                reversed == null ? Collections.emptyList() : reversed);\n        deletedRanges = normalized.deletedRanges;\n        reversedRanges = normalized.reversedRanges;\n        positionSeconds = nearestKeptSource(positionSeconds);\n        invalidate();\n    }\n\n    double getVisibleDurationSeconds() {\n        return visibleDurationSeconds();\n    }\n\n    double getVisibleOffsetSeconds(double sourceSeconds) {\n        return visibleOffsetForSource(sourceSeconds);\n    }''',
        "timeline setRanges",
    )

    text = replace_once(
        text,
        '''        for (AnimationEdits.TimeRange range : reversedRanges) {\n            drawRange(canvas, range, 0xFF7C6CE7, thickness);\n        }\n        for (AnimationEdits.TimeRange range : deletedRanges) {\n            drawRange(canvas, range, 0xFFE76B6B, thickness);\n        }''',
        '''        for (AnimationEdits.TimeRange range : reversedRanges) {\n            drawRange(canvas, range, 0xFF7C6CE7, thickness);\n        }''',
        "remove red deleted ranges",
    )

    text = replace_once(
        text,
        '''    private void updateTouchPosition(float touchX, boolean finished) {\n        float left = dp(8);\n        float right = Math.max(left + 1f, getWidth() - dp(8));\n        float normalized = (touchX - left) / (right - left);\n        normalized = Math.max(0f, Math.min(1f, normalized));\n        positionSeconds = normalized * durationSeconds;\n        invalidate();\n        if (seekListener != null) seekListener.onSeek(positionSeconds, finished);\n    }\n\n    @Override\n    public boolean performClick() {\n        super.performClick();\n        return true;\n    }\n\n    private float xFor(double seconds) {\n        float left = dp(8);\n        float right = Math.max(left + 1f, getWidth() - dp(8));\n        double normalized = clamp(seconds) / durationSeconds;\n        return left + (float) normalized * (right - left);\n    }\n\n    private double clamp(double value) {\n        return Math.max(0.0, Math.min(durationSeconds, value));\n    }''',
        '''    private void updateTouchPosition(float touchX, boolean finished) {\n        float left = dp(8);\n        float right = Math.max(left + 1f, getWidth() - dp(8));\n        float normalized = (touchX - left) / (right - left);\n        normalized = Math.max(0f, Math.min(1f, normalized));\n        positionSeconds = sourceForVisibleOffset(normalized * visibleDurationSeconds());\n        invalidate();\n        if (seekListener != null) seekListener.onSeek(positionSeconds, finished);\n    }\n\n    @Override\n    public boolean performClick() {\n        super.performClick();\n        return true;\n    }\n\n    private float xFor(double seconds) {\n        float left = dp(8);\n        float right = Math.max(left + 1f, getWidth() - dp(8));\n        double normalized = visibleOffsetForSource(seconds) / visibleDurationSeconds();\n        return left + (float) normalized * (right - left);\n    }\n\n    private double visibleDurationSeconds() {\n        double removed = 0.0;\n        for (AnimationEdits.TimeRange range : deletedRanges) {\n            double start = Math.max(0.0, Math.min(durationSeconds, range.startSeconds));\n            double end = Math.max(start, Math.min(durationSeconds, range.endSeconds));\n            removed += Math.max(0.0, end - start);\n        }\n        return Math.max(0.001, durationSeconds - removed);\n    }\n\n    private double visibleOffsetForSource(double sourceSeconds) {\n        double source = clamp(sourceSeconds);\n        double removed = 0.0;\n        for (AnimationEdits.TimeRange range : deletedRanges) {\n            double start = Math.max(0.0, Math.min(durationSeconds, range.startSeconds));\n            double end = Math.max(start, Math.min(durationSeconds, range.endSeconds));\n            if (source >= end) removed += end - start;\n            else if (source > start) {\n                removed += source - start;\n                break;\n            } else break;\n        }\n        return Math.max(0.0, Math.min(visibleDurationSeconds(), source - removed));\n    }\n\n    private double sourceForVisibleOffset(double visibleSeconds) {\n        double remaining = Math.max(0.0, Math.min(visibleDurationSeconds(), visibleSeconds));\n        double cursor = 0.0;\n        for (AnimationEdits.TimeRange range : deletedRanges) {\n            double start = Math.max(cursor, Math.min(durationSeconds, range.startSeconds));\n            double end = Math.max(start, Math.min(durationSeconds, range.endSeconds));\n            double kept = Math.max(0.0, start - cursor);\n            if (remaining <= kept) return clamp(cursor + remaining);\n            remaining -= kept;\n            cursor = end;\n        }\n        return clamp(cursor + remaining);\n    }\n\n    private double nearestKeptSource(double sourceSeconds) {\n        double source = clamp(sourceSeconds);\n        for (AnimationEdits.TimeRange range : deletedRanges) {\n            if (source >= range.startSeconds && source < range.endSeconds) {\n                if (range.endSeconds < durationSeconds) return clamp(range.endSeconds);\n                return clamp(Math.max(0.0, range.startSeconds - 0.001));\n            }\n        }\n        return source;\n    }\n\n    private double clamp(double value) {\n        return Math.max(0.0, Math.min(durationSeconds, value));\n    }''',
        "timeline collapsed coordinate mapping",
    )

    # ------------------------------------------------------------------
    # 2) Video preview: add a second audio-only Media3 player for BGM.
    # ------------------------------------------------------------------
    text = insert_after(
        text,
        '''    private ExoPlayer audioPlayer;\n''',
        '''    private ExoPlayer musicPlayer;\n    private Uri previewMusicUri;\n    private float previewMusicVolume = 0.5f;\n    private boolean previewMusicLoop = true;\n    private long previewMusicStartMs;\n    private long previewFadeMs;\n    private long mixPositionMs;\n    private long mixDurationMs;\n    private long musicGeneration;\n''',
        "music preview fields",
    )

    text = insert_after(
        text,
        '''    void setPreviewVolume(float volume) {\n        previewVolume = Math.max(0f, Math.min(1f, volume));\n        if (audioPlayer != null) {\n            try { audioPlayer.setVolume(previewVolume); }\n            catch (RuntimeException error) { fallbackAudio("原声预览暂不可用，可继续剪辑"); }\n        }\n    }\n''',
        r'''

    void setBackgroundMusic(Uri music, float volume, boolean loop,
                            double startSeconds, double fadeSeconds) {
        previewMusicUri = music;
        previewMusicVolume = Math.max(0f, Math.min(1f, volume));
        previewMusicLoop = loop;
        previewMusicStartMs = Math.max(0L, Math.round(startSeconds * 1000.0));
        previewFadeMs = Math.max(0L, Math.round(fadeSeconds * 1000.0));
        prepareMusic();
    }

    void setBackgroundTimelinePosition(int positionMs, int totalDurationMs) {
        mixPositionMs = Math.max(0L, positionMs);
        mixDurationMs = Math.max(0L, totalDurationMs);
        syncMusic(false);
    }

    private void prepareMusic() {
        releaseMusic();
        if (detached || previewMusicUri == null || previewMusicVolume <= 0f) return;
        final long generation = ++musicGeneration;
        try {
            ExoPlayer player = new ExoPlayer.Builder(getContext().getApplicationContext(),
                    new DefaultRenderersFactory(getContext().getApplicationContext())
                            .setEnableDecoderFallback(true))
                    .setLoadControl(new DefaultLoadControl.Builder()
                            .setBufferDurationsMs(1000, 5000, 250, 500).build())
                    .build();
            musicPlayer = player;
            player.setTrackSelectionParameters(player.getTrackSelectionParameters().buildUpon()
                    .setTrackTypeDisabled(C.TRACK_TYPE_VIDEO, true)
                    .setTrackTypeDisabled(C.TRACK_TYPE_TEXT, true)
                    .setTrackTypeDisabled(C.TRACK_TYPE_IMAGE, true)
                    .build());
            // The source player owns audio focus. The music player is mixed alongside it so the
            // two players never pause each other while previewing.
            player.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(C.USAGE_MEDIA).setContentType(C.AUDIO_CONTENT_TYPE_MUSIC).build(), false);
            player.setHandleAudioBecomingNoisy(true);
            player.addListener(new Player.Listener() {
                private boolean current() {
                    return !detached && musicGeneration == generation && musicPlayer == player;
                }
                @Override public void onPlayerError(PlaybackException error) {
                    if (current()) releaseMusic();
                }
                @Override public void onPlaybackStateChanged(int state) {
                    if (!current()) return;
                    if (state == Player.STATE_READY) syncMusic(true);
                    else if (state == Player.STATE_ENDED && previewMusicLoop && logicalPlaying) {
                        syncMusic(true);
                    }
                }
            });
            player.setMediaItem(MediaItem.fromUri(previewMusicUri));
            player.prepare();
        } catch (RuntimeException | LinkageError error) {
            releaseMusic();
        }
    }

    private void syncMusic(boolean forceSeek) {
        ExoPlayer player = musicPlayer;
        if (player == null) return;
        try {
            long duration = player.getDuration();
            if (duration <= 0 || duration == C.TIME_UNSET) return;
            long start = Math.min(Math.max(0L, previewMusicStartMs), Math.max(0L, duration - 1L));
            long available = Math.max(1L, duration - start);
            long target;
            boolean audible = true;
            if (previewMusicLoop) {
                target = start + (mixPositionMs % available);
            } else {
                long raw = start + mixPositionMs;
                audible = raw < duration;
                target = Math.min(Math.max(start, raw), Math.max(start, duration - 1L));
            }
            long fade = previewFadeMs;
            float fadeGain = 1f;
            if (fade > 0 && mixDurationMs > 0) {
                float in = Math.min(1f, mixPositionMs / (float) fade);
                float out = Math.min(1f, Math.max(0L, mixDurationMs - mixPositionMs) / (float) fade);
                fadeGain = Math.max(0f, Math.min(in, out));
            }
            player.setVolume(audible ? previewMusicVolume * fadeGain : 0f);
            long drift = Math.abs(player.getCurrentPosition() - target);
            if (forceSeek || drift > 350L) player.seekTo(target);
            if (logicalPlaying && audible) player.play();
            else player.pause();
        } catch (RuntimeException error) {
            releaseMusic();
        }
    }

    private void releaseMusic() {
        musicGeneration++;
        ExoPlayer old = musicPlayer;
        musicPlayer = null;
        if (old != null) { try { old.release(); } catch (RuntimeException ignored) { } }
    }
''',
        "music preview methods",
    )

    text = replace_once(
        text,
        '''        if (audioPlayer != null) {\n            try {\n                audioPlayer.seekTo(position);\n                audioPlayer.play();\n            } catch (RuntimeException error) { fallbackAudio("播放原声失败，已切换为静音预览"); }\n        }\n        requestFrame(position);''',
        '''        if (audioPlayer != null) {\n            try {\n                audioPlayer.seekTo(position);\n                audioPlayer.play();\n            } catch (RuntimeException error) { fallbackAudio("播放原声失败，已切换为静音预览"); }\n        }\n        syncMusic(true);\n        requestFrame(position);''',
        "start music with preview",
    )

    text = replace_once(
        text,
        '''        if (audioPlayer != null) {\n            try { audioPlayer.pause(); }\n            catch (RuntimeException error) { fallbackAudio("原声预览暂不可用，可继续剪辑"); }\n        }\n        requestFrame(basePositionMs);''',
        '''        if (audioPlayer != null) {\n            try { audioPlayer.pause(); }\n            catch (RuntimeException error) { fallbackAudio("原声预览暂不可用，可继续剪辑"); }\n        }\n        if (musicPlayer != null) {\n            try { musicPlayer.pause(); } catch (RuntimeException error) { releaseMusic(); }\n        }\n        requestFrame(basePositionMs);''',
        "pause music with preview",
    )

    text = replace_once(
        text,
        '''        if (audioPlayer != null) {\n            try { audioPlayer.pause(); } catch (RuntimeException ignored) { releaseAudio(); }\n        }\n        requestFrame(Math.max(0, durationMs - 1));''',
        '''        if (audioPlayer != null) {\n            try { audioPlayer.pause(); } catch (RuntimeException ignored) { releaseAudio(); }\n        }\n        if (musicPlayer != null) {\n            try { musicPlayer.pause(); } catch (RuntimeException ignored) { releaseMusic(); }\n        }\n        requestFrame(Math.max(0, durationMs - 1));''',
        "finish music with preview",
    )

    text = replace_once(
        text,
        '''        releaseAudio();\n        mainHandler.removeCallbacksAndMessages(null);\n        renderer.close();''',
        '''        releaseAudio();\n        releaseMusic();\n        mainHandler.removeCallbacksAndMessages(null);\n        renderer.close();''',
        "release music on stopPlayback",
    )

    text = replace_once(
        text,
        '''        releaseAudio();\n        audioStatusListener = null;\n        mainHandler.removeCallbacksAndMessages(null);''',
        '''        releaseAudio();\n        releaseMusic();\n        audioStatusListener = null;\n        mainHandler.removeCallbacksAndMessages(null);''',
        "release music on detach",
    )

    # ------------------------------------------------------------------
    # 3) Main UI: dynamic format list, safer spinner gestures, compact help,
    #    clearer edit button.
    # ------------------------------------------------------------------
    text = insert_after(
        text,
        '''    private Spinner formatSpinner;\n''',
        '''    private final List<Integer> visibleOutputFormats = new ArrayList<>();\n    private boolean refreshingOutputFormats;\n''',
        "dynamic output fields",
    )

    text = replace_once(
        text,
        '''        TextView selectionHint = text(\n                "再次添加会保留当前选择；长按文件卡片拖动排序。生成 GIF 时按列表顺序播放。",\n                12, SECONDARY_TEXT, false);''',
        '''        TextView selectionHint = text(\n                "长按文件卡片可拖动排序。",\n                12, SECONDARY_TEXT, false);''',
        "short selection hint",
    )

    text = replace_once(
        text,
        '''        addLabel(panel, "输出格式", PRIMARY_TEXT);\n        formatSpinner = createSpinner(OUTPUT_FORMATS);''',
        '''        addLabel(panel, "输出格式", PRIMARY_TEXT);\n        visibleOutputFormats.clear();\n        for (int i = 0; i < OUTPUT_FORMATS.length; i++) visibleOutputFormats.add(i);\n        formatSpinner = createSpinner(OUTPUT_FORMATS);''',
        "initialize output mapping",
    )

    text = replace_once(
        text,
        '''        TextView hint = text(\n                "导入视频后自动打开剪辑；也可随时点“视频 / GIF 剪辑”。剪辑内可设置声音、配乐并直接导出 MP4。",\n                12, SECONDARY_TEXT, false);''',
        '''        TextView hint = text(\n                "视频 / GIF 可继续剪辑或直接导出。",\n                12, SECONDARY_TEXT, false);''',
        "short editor hint",
    )

    text = replace_section(
        text,
        '''        LinearLayout helpPanel = new LinearLayout(this);''',
        '''        helpPanel.addView(codecSupportText);''',
        '''        TextView simpleHelp = text(\n                "导入文件后只显示可用输出格式；视频剪辑可处理原声、配乐和片段。",\n                12, SECONDARY_TEXT, false);\n        simpleHelp.setPadding(0, dp(12), 0, 0);\n        root.addView(simpleHelp, matchWrap());\n        codecSupportText = text("", 1, SECONDARY_TEXT, false);\n        codecSupportText.setVisibility(View.GONE);\n        root.addView(codecSupportText, matchWrap());''',
        "compact main help",
    )

    text = replace_once(
        text,
        '''            @Override public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {\n                updateControlStates();\n            }''',
        '''            @Override public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {\n                if (!refreshingOutputFormats) updateControlStates();\n            }''',
        "spinner refresh guard",
    )

    # These reads must use the stable format id rather than the filtered spinner position.
    for old, new, label in [
        ("int format = formatSpinner.getSelectedItemPosition();", "int format = selectedOutputFormat();", "control selected format"),
        ("final int format=formatSpinner.getSelectedItemPosition();", "final int format=selectedOutputFormat();", "recommendation selected format"),
        ("int selectedFormat = formatSpinner.getSelectedItemPosition();", "int selectedFormat = selectedOutputFormat();", "conversion selected format"),
        ("int existingFormat = formatSpinner.getSelectedItemPosition();", "int existingFormat = selectedOutputFormat();", "editor existing format"),
        ("beginConversionInternal(batchMode, selectedItems, formatSpinner.getSelectedItemPosition());", "beginConversionInternal(batchMode, selectedItems, selectedOutputFormat());", "internal conversion selected format"),
        ("int format = formatSpinner == null ? 0 : formatSpinner.getSelectedItemPosition();", "int format = selectedOutputFormat();", "action selected format"),
    ]:
        text = replace_once(text, old, new, label)

    text = replace_once(text, "formatSpinner.setSelection(3);", "setSelectedOutputFormat(3);", "shared-video format selection")
    text = replace_once(text, "formatSpinner.setSelection(outputFormat);", "setSelectedOutputFormat(outputFormat);", "editor export format selection")

    # Add format helpers immediately before updateControlStates.
    text = replace_once(
        text,
        '''    private void updateControlStates() {''',
        r'''    private int selectedOutputFormat() {
        if (formatSpinner == null || visibleOutputFormats.isEmpty()) return -1;
        int position = formatSpinner.getSelectedItemPosition();
        if (position < 0 || position >= visibleOutputFormats.size()) return -1;
        return visibleOutputFormats.get(position);
    }

    private void setSelectedOutputFormat(int format) {
        if (formatSpinner == null) return;
        int position = visibleOutputFormats.indexOf(format);
        if (position >= 0) formatSpinner.setSelection(position);
    }

    private void refreshOutputFormatOptions() {
        if (formatSpinner == null || refreshingOutputFormats) return;
        int previous = selectedOutputFormat();
        List<Integer> next = new ArrayList<>();
        for (int i = 0; i < OUTPUT_FORMATS.length; i++) {
            if (selectedItems.isEmpty() || isOutputFormatCompatible(i)) next.add(i);
        }
        if (next.equals(visibleOutputFormats)) {
            formatSpinner.setEnabled(!busy && !next.isEmpty());
            return;
        }
        List<String> labels = new ArrayList<>();
        for (int format : next) labels.add(OUTPUT_FORMATS[format]);
        if (labels.isEmpty()) labels.add("当前文件组合没有可直接转换的格式");
        refreshingOutputFormats = true;
        visibleOutputFormats.clear();
        visibleOutputFormats.addAll(next);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, labels);
        formatSpinner.setAdapter(adapter);
        int position = visibleOutputFormats.indexOf(previous);
        if (position < 0 && !visibleOutputFormats.isEmpty()) position = 0;
        if (position >= 0) formatSpinner.setSelection(position, false);
        formatSpinner.setEnabled(!busy && !visibleOutputFormats.isEmpty());
        refreshingOutputFormats = false;
    }

    private boolean isOutputFormatCompatible(int format) {
        if (selectedItems.isEmpty()) return true;
        int videoCount = 0, pdfCount = 0, textCount = 0, audioCount = 0;
        for (SelectedItem item : selectedItems) {
            if (item.isVideo()) videoCount++;
            else if (item.sourceFormat == SourceFormat.AUDIO) audioCount++;
            else if (item.sourceFormat == SourceFormat.PDF) pdfCount++;
            else if (isTextSourceFormat(item.sourceFormat)) textCount++;
        }
        if (isTextOutputFormat(format)) {
            if (textCount + pdfCount != selectedItems.size()) return false;
            for (SelectedItem item : selectedItems) {
                if (!textConversionSupported(format, item.sourceFormat)) return false;
            }
            return true;
        }
        if (textCount > 0) return false;
        if (format == 9 || format == 10 || format == 27) {
            if (selectedItems.size() != 1) return false;
            SelectedItem item = selectedItems.get(0);
            return item.isVideo() || item.sourceFormat == SourceFormat.AUDIO;
        }
        if (audioCount > 0) return false;
        if (format == 11) {
            if (videoCount > 0) return false;
            if (pdfCount > 0) return pdfCount == selectedItems.size() && pdfCount >= 2;
            return true;
        }
        if (format == 12) return videoCount == 0 && pdfCount == 0;
        if (format >= 4 && format <= 6) {
            if (format == 4 && !h264Supported) return false;
            if (format == 5 && !h265Supported) return false;
            if (format == 6 && !av1Supported) return false;
            return hasOnlyVideosSelected()
                    || (selectedItems.size() == 1
                    && selectedItems.get(0).sourceFormat == SourceFormat.GIF);
        }
        if (format == 3) {
            if (pdfCount > 0) return false;
            if (videoCount > 0) return videoCount == selectedItems.size();
            if (selectedItems.size() == 1) {
                return selectedItems.get(0).sourceFormat == SourceFormat.GIF;
            }
            return selectedItems.size() > 1;
        }
        if (isStaticOutputFormat(format)) {
            if (videoCount > 0) return false;
            if (pdfCount > 0) return pdfCount == selectedItems.size();
            return true;
        }
        return false;
    }

    private void updateControlStates() {''',
        "output filtering helpers",
    )

    # updateSelectionUi: refresh the format list before control/action calculation.
    text = replace_once(
        text,
        '''        clearButton.setEnabled(!busy && !selectedItems.isEmpty());\n        applyButtonStyle(clearButton, clearButton.isEnabled(), false);\n        updateControlStates();''',
        '''        clearButton.setEnabled(!busy && !selectedItems.isEmpty());\n        applyButtonStyle(clearButton, clearButton.isEnabled(), false);\n        refreshOutputFormatOptions();\n        updateControlStates();''',
        "refresh format list on selection change",
    )

    # No format can exist for deliberately incompatible mixed selections.
    text = replace_once(
        text,
        '''        int format = selectedOutputFormat();\n        boolean jpeg = format == 0;''',
        '''        int format = selectedOutputFormat();\n        if (format < 0) {\n            setViewsVisible(false, qualityText, qualitySeek, resolutionLabel, resolutionSpinner,\n                    resolutionCustomRow, fpsLabel, fpsSpinner, customFpsEdit, frameLimitLabel,\n                    frameLimitSpinner, customFrameLimitEdit, bitrateLabel, bitrateSpinner,\n                    customBitrateEdit, loopLabel, loopSpinner, customLoopEdit, videoGifOutputLabel,\n                    videoGifOutputSpinner, videoLoopLabel, videoLoopSpinner, customVideoLoopEdit,\n                    reverseLoopLabel, reverseLoopSpinner, customReverseLoopEdit, animationOptionsHint);\n            boolean canManualEdit = hasTimedSourceSelected();\n            setViewsVisible(canManualEdit, editButton);\n            if (editButton != null) {\n                editButton.setEnabled(!busy && canManualEdit);\n                applyEditButtonStyle(editButton, !busy && canManualEdit);\n            }\n            recommendationText.setText("当前文件组合没有可用输出格式");\n            updateActionState();\n            return;\n        }\n        boolean jpeg = format == 0;''',
        "no-compatible-format control state",
    )

    text = replace_once(text, "applyButtonStyle(editButton, canManualEdit, false);", "applyEditButtonStyle(editButton, canManualEdit);", "edit button enabled style")
    text = replace_once(text, "applyButtonStyle(editButton, false, false);", "applyEditButtonStyle(editButton, false);", "edit button disabled style")

    text = replace_once(
        text,
        '''        formatSpinner.setEnabled(!value);''',
        '''        formatSpinner.setEnabled(!value && !visibleOutputFormats.isEmpty());''',
        "busy filtered spinner state",
    )

    text = replace_once(
        text,
        '''        statusText.setText(state.reason);''',
        '''        statusText.setText(state.enabled ? "" : state.reason);\n        statusText.setVisibility(state.enabled ? View.GONE : View.VISIBLE);''',
        "compact action status",
    )

    text = replace_once(
        text,
        '''        int format = selectedOutputFormat();\n        int videoCount = 0;''',
        '''        int format = selectedOutputFormat();\n        if (format < 0) {\n            return ActionState.disabled("当前文件组合没有可直接转换的格式，请移除不兼容的文件。");\n        }\n        int videoCount = 0;''',
        "evaluate no format",
    )

    # scheduleRecommendation must not interpret a filtered spinner position as a format id.
    text = replace_once(
        text,
        '''        final int format=selectedOutputFormat();\n        final int resolution=resolutionSpinner.getSelectedItemPosition();''',
        '''        final int format=selectedOutputFormat();\n        if (format < 0) { recommendationText.setText("当前文件组合没有可用输出格式"); return; }\n        final int resolution=resolutionSpinner.getSelectedItemPosition();''',
        "recommendation no format",
    )

    # refreshCodecSupportText is hidden now but still performs capability probing; refresh choices.
    text = replace_once(
        text,
        '''        codecSupportText.setText(\n                "本机编码器：H.264 " + supportWord(h264Supported)\n                        + "　H.265 " + supportWord(h265Supported)\n                        + "　AV1 " + supportWord(av1Supported));\n        updateActionState();''',
        '''        codecSupportText.setText(\n                "本机编码器：H.264 " + supportWord(h264Supported)\n                        + "　H.265 " + supportWord(h265Supported)\n                        + "　AV1 " + supportWord(av1Supported));\n        refreshOutputFormatOptions();\n        updateActionState();''',
        "refresh filtered formats after codec probe",
    )

    # Safer secondary edit button style.
    text = insert_after(
        text,
        '''    private void applyButtonStyle(Button button, boolean enabled, boolean primary) {\n        button.setTextColor(0xFFFFFFFF);\n        int color;\n        if (!enabled) color = DISABLED;\n        else color = primary ? PRIMARY : 0xFF777A88;\n        button.setBackground(roundRect(color, 14));\n        button.setAlpha(1f);\n    }\n''',
        r'''

    private void applyEditButtonStyle(Button button, boolean enabled) {
        GradientDrawable background = roundRect(enabled ? 0xFFF0EFFF : 0xFFF0F1F5, 14);
        background.setStroke(dp(1), enabled ? PRIMARY : 0xFFD3D5DD);
        button.setBackground(background);
        button.setTextColor(enabled ? PRIMARY : 0xFF8A8C96);
        button.setAlpha(1f);
    }
''',
        "edit button accent style",
    )

    # All Spinners suppress a click when the same gesture was actually a scroll.
    text = replace_once(
        text,
        '''    private Spinner createSpinner(String[] values) {\n        Spinner spinner = new Spinner(this);\n        ArrayAdapter<String> adapter = new ArrayAdapter<>(\n                this, android.R.layout.simple_spinner_dropdown_item, values);\n        spinner.setAdapter(adapter);\n        return spinner;\n    }''',
        r'''    private Spinner createSpinner(String[] values) {
        Spinner spinner = new Spinner(this);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(
                this, android.R.layout.simple_spinner_dropdown_item, values);
        spinner.setAdapter(adapter);
        final float[] down = new float[2];
        final boolean[] moved = {false};
        final int slop = android.view.ViewConfiguration.get(this).getScaledTouchSlop();
        spinner.setOnTouchListener((view, event) -> {
            switch (event.getActionMasked()) {
                case android.view.MotionEvent.ACTION_DOWN:
                    down[0] = event.getRawX();
                    down[1] = event.getRawY();
                    moved[0] = false;
                    return false;
                case android.view.MotionEvent.ACTION_MOVE:
                    if (Math.abs(event.getRawY() - down[1]) > slop
                            || Math.abs(event.getRawX() - down[0]) > slop) {
                        moved[0] = true;
                        view.setPressed(false);
                    }
                    return false;
                case android.view.MotionEvent.ACTION_UP:
                    boolean consume = moved[0];
                    moved[0] = false;
                    if (consume) view.setPressed(false);
                    return consume;
                case android.view.MotionEvent.ACTION_CANCEL:
                    moved[0] = false;
                    view.setPressed(false);
                    return false;
                default:
                    return false;
            }
        });
        return spinner;
    }''',
        "spinner scroll gesture guard",
    )

    # ------------------------------------------------------------------
    # 4) Editor integration: sync BGM, skip deleted media during playback,
    #    and shorten verbose in-dialog explanations.
    # ------------------------------------------------------------------
    text = replace_once(
        text,
        '''        TextView cutHelp = text(\n                "拖动视频底部时间轴定位；“分割”会留下切点。删除会按当前光标所在分段执行，红色表示删除区间，紫色表示倒放区间。",\n                12, SECONDARY_TEXT, false);''',
        '''        TextView cutHelp = text(\n                "拖动时间轴定位；分割后可删除或倒放，撤销可恢复。",\n                12, SECONDARY_TEXT, false);''',
        "short cut help",
    )

    text = replace_once(
        text,
        '''        content.addView(text("预览播放素材原声；截取、变速、删除、倒放和配乐混音以导出结果为准。",\n                11, SECONDARY_TEXT, false), matchWrap());''',
        '''        content.addView(text("预览同步播放原声和背景音乐；导出时应用完整剪辑与混音。",\n                11, SECONDARY_TEXT, false), matchWrap());''',
        "short audio preview hint",
    )

    text = replace_once(
        text,
        '''        refreshEditorAudio = () -> {\n            if (videoPreview[0] != null) videoPreview[0].setPreviewVolume(originalVolume);\n            editorAudio.setText(backgroundMusic == null ? "声音设置 / 添加背景音乐"\n                    : "声音设置 · 已添加背景音乐");\n        };''',
        '''        refreshEditorAudio = () -> {\n            if (videoPreview[0] != null) {\n                videoPreview[0].setPreviewVolume(originalVolume);\n                videoPreview[0].setBackgroundMusic(backgroundMusic, musicVolume, musicLoop,\n                        musicStartSeconds, audioFadeSeconds);\n            }\n            editorAudio.setText(backgroundMusic == null ? "声音设置 / 添加背景音乐"\n                    : "声音设置 · 已添加背景音乐");\n        };''',
        "editor BGM refresh",
    )

    # Any explicit seek into a deleted source range snaps to the nearest kept edge.
    text = replace_once(
        text,
        '''        final java.util.function.DoubleConsumer seekPreviewTo = secondsValue -> {\n            double seconds = Math.max(0.0, Math.min(timelineSeconds, secondsValue));\n            timeline.setPositionSeconds(seconds);''',
        '''        final java.util.function.DoubleConsumer seekPreviewTo = secondsValue -> {\n            double seconds = Math.max(0.0, Math.min(timelineSeconds, secondsValue));\n            for (AnimationEdits.TimeRange deleted : deletedRanges) {\n                if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {\n                    seconds = deleted.endSeconds < timelineSeconds\n                            ? deleted.endSeconds : Math.max(0.0, deleted.startSeconds - 0.001);\n                    break;\n                }\n            }\n            timeline.setPositionSeconds(seconds);''',
        "snap seeks past deleted ranges",
    )

    # Keep BGM aligned to the compressed (kept) timeline after each explicit seek.
    text = replace_once(
        text,
        '''                updatePreviewVisual[0].run();\n            } else if (gifPreview[0] != null) {''',
        '''                updatePreviewVisual[0].run();\n                int mixMs = (int) Math.min(Integer.MAX_VALUE,\n                        Math.round(timeline.getVisibleOffsetSeconds(seconds) * 1000.0));\n                int mixDurationMs = (int) Math.min(Integer.MAX_VALUE,\n                        Math.round(timeline.getVisibleDurationSeconds() * 1000.0));\n                videoPreview[0].setBackgroundTimelinePosition(mixMs, mixDurationMs);\n            } else if (gifPreview[0] != null) {''',
        "sync BGM on seek",
    )

    # Playback ticker skips ranges that no longer exist and continuously keeps music in sync.
    text = replace_once(
        text,
        '''                    seconds = Math.max(0.0, Math.min(timelineSeconds, seconds));\n                    timeline.setPositionSeconds(seconds);\n                    if (!videoPreview[0].isPlaying()) {''',
        '''                    seconds = Math.max(0.0, Math.min(timelineSeconds, seconds));\n                    double skippedTo = seconds;\n                    for (AnimationEdits.TimeRange deleted : deletedRanges) {\n                        if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {\n                            skippedTo = Math.min(timelineSeconds, deleted.endSeconds);\n                            break;\n                        }\n                    }\n                    if (skippedTo > seconds + 0.0005) {\n                        seekPreviewTo.accept(skippedTo);\n                        seconds = skippedTo;\n                    } else {\n                        timeline.setPositionSeconds(seconds);\n                    }\n                    int mixMs = (int) Math.min(Integer.MAX_VALUE,\n                            Math.round(timeline.getVisibleOffsetSeconds(seconds) * 1000.0));\n                    int mixDurationMs = (int) Math.min(Integer.MAX_VALUE,\n                            Math.round(timeline.getVisibleDurationSeconds() * 1000.0));\n                    videoPreview[0].setBackgroundTimelinePosition(mixMs, mixDurationMs);\n                    if (!videoPreview[0].isPlaying()) {''',
        "skip deleted video and sync BGM ticker",
    )

    # GIF preview also jumps over deleted source ranges.
    text = replace_once(
        text,
        '''                } else if (gifPreview[0] != null) {\n                    seconds = gifPreview[0].getCurrentPosition() / 1000.0;\n                    timeline.setPositionSeconds(seconds);\n                }''',
        '''                } else if (gifPreview[0] != null) {\n                    seconds = gifPreview[0].getCurrentPosition() / 1000.0;\n                    double skippedTo = seconds;\n                    for (AnimationEdits.TimeRange deleted : deletedRanges) {\n                        if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {\n                            skippedTo = Math.min(timelineSeconds, deleted.endSeconds);\n                            break;\n                        }\n                    }\n                    if (skippedTo > seconds + 0.0005) {\n                        seekPreviewTo.accept(skippedTo);\n                        seconds = skippedTo;\n                    } else {\n                        timeline.setPositionSeconds(seconds);\n                    }\n                }''',
        "skip deleted gif ticker",
    )

    # When a deletion is made, jump to the next kept frame (or just before an end cut).
    text = replace_once(
        text,
        '''            seekPreviewTo.accept(Math.min(timelineSeconds, startPoint));\n            updateTimelineState.run();''',
        '''            double resumePoint = endPoint < timelineSeconds - 0.001\n                    ? endPoint : Math.max(0.0, startPoint - 0.001);\n            seekPreviewTo.accept(Math.min(timelineSeconds, resumePoint));\n            updateTimelineState.run();''',
        "jump past deleted segment",
    )

    # Keep BGM mapping correct after delete/undo/redo changes the visible duration.
    text = replace_once(
        text,
        '''            timeline.setSplitPoints(splitPoints[0], splitPoints[1]);\n            timeline.setRanges(deletedRanges, reversedRanges);\n            boolean hasFirstPoint''',
        '''            timeline.setSplitPoints(splitPoints[0], splitPoints[1]);\n            timeline.setRanges(deletedRanges, reversedRanges);\n            if (videoPreview[0] != null) {\n                double source = previewVideoIndex[0] >= 0\n                        ? previewVideoOffsetSeconds[0] + videoPreview[0].getCurrentPosition() / 1000.0\n                        : timeline.getPositionSeconds();\n                videoPreview[0].setBackgroundTimelinePosition(\n                        (int) Math.min(Integer.MAX_VALUE, Math.round(\n                                timeline.getVisibleOffsetSeconds(source) * 1000.0)),\n                        (int) Math.min(Integer.MAX_VALUE, Math.round(\n                                timeline.getVisibleDurationSeconds() * 1000.0)));\n            }\n            boolean hasFirstPoint''',
        "resync BGM after timeline edit",
    )

    text = replace_once(
        text,
        '''        content.addView(text("按当前主页的分辨率、帧率、码率和帧数上限导出；多个视频按列表顺序合并。",\n                11, SECONDARY_TEXT, false), matchWrap());''',
        '''        content.addView(text("使用主页当前视频参数；多视频按列表顺序合并。",\n                11, SECONDARY_TEXT, false), matchWrap());''',
        "short direct export hint",
    )

    text = replace_once(
        text,
        '''        TextView colorHint = text(\n                "为保证不同手机上的视频预览稳定，调色参数保存后会准确应用到最终输出。",\n                11, SECONDARY_TEXT, false);''',
        '''        TextView colorHint = text(\n                "调色会应用到最终输出。",\n                11, SECONDARY_TEXT, false);''',
        "short color hint",
    )

    text = replace_once(
        text,
        '''        TextView help=text("导出 MP4 时生效。原声与背景音乐分别调节；0% 为静音。自动转成 AAC-LC 48 kHz / 192 kbps。变速保持音调，倒放片段同步倒放原声。预览可播放原声（试听音量最高 100%，避免过响）；配乐、淡入淡出和倒放混音在导出时合成。",13,SECONDARY_TEXT,false);content.addView(help);''',
        '''        TextView help=text("原声和背景音乐可分别调音量；预览会同步播放，导出时应用循环和淡入淡出。",13,SECONDARY_TEXT,false);content.addView(help);''',
        "short sound settings help",
    )

    # README statements should match the new preview behavior and collapsed deletion UI.
    text = text.replace(
        "- 预览播放素材原声；配乐、变速、倒放等最终混音在导出时合成，预览音量最高 100%，导出仍支持 0–200%。",
        "- 预览同步播放素材原声与背景音乐；导出仍支持完整混音、循环、淡入淡出和 0–200% 音量。",
    )
    text = text.replace(
        "剪辑预览使用兼容画面渲染并播放素材原声；配乐与剪辑混音在导出时合成。硬件编码、音频解码能力受手机影响。AV1 输出仍依赖 Android 14+ 与可用编码器。",
        "剪辑预览使用兼容画面渲染并同步播放原声与背景音乐；删除片段会从时间轴折叠消失并可撤销。硬件编码、音频解码能力受手机影响。AV1 输出仍依赖 Android 14+ 与可用编码器。",
    )

    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="android_project.py")
    parser.add_argument("--check", action="store_true", help="validate patch without writing")
    parser.add_argument("--backup", action="store_true", help="write <file>.bak before replacing")
    args = parser.parse_args()

    path = Path(args.path)
    source = path.read_text(encoding="utf-8")
    patched = apply_patch(source)
    if patched == source:
        raise RuntimeError("patch produced no changes")
    # Fast structural checks for the most important changes.
    required = [
        "selectedOutputFormat()",
        "refreshOutputFormatOptions()",
        "setBackgroundMusic(Uri music",
        "getVisibleDurationSeconds()",
        "spinner.setOnTouchListener",
        "applyEditButtonStyle",
        "预览同步播放原声和背景音乐",
    ]
    missing = [item for item in required if item not in patched]
    if missing:
        raise RuntimeError("patched source is missing: " + ", ".join(missing))
    if args.check:
        print("[OK] android_project.py patch validated")
        return
    if args.backup:
        path.with_suffix(path.suffix + ".bak").write_text(source, encoding="utf-8")
    path.write_text(patched, encoding="utf-8")
    print(f"[OK] patched {path} ({len(source):,} -> {len(patched):,} chars)")


if __name__ == "__main__":
    main()
