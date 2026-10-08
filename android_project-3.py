#!/usr/bin/env python3
"""Format Converter v8.2 — readable, self-contained Android project generator.

Usage: python android_project.py --output .
Edit the source strings below; generated Gradle/app directories are build outputs.
The second build file is .github/workflows/build.yml. The repository image 转换.png
is the only image input; original app capabilities are retained.
"""
from pathlib import Path
import argparse

SOURCES = {
    'README.md': r'''# 格式转换器 Android v8.2

全部转换在本机完成。最低 Android 9（API 28），目标 Android 16（API 36）。

构建只需两个文件：

- `.github/workflows/build.yml`：GitHub Actions 构建、测试、APK 验签和产物上传。
- `android_project.py`：可读的完整 Java 源码、资源、依赖和测试；运行后生成安卓项目。

本次同时替换以上两个文件，保留当前文件名和路径。根目录 `转换.png` 自动生成各 DPI 和自适应桌面图标。修改以上文件或图标会触发构建，也可在 Actions 手动运行。下载 `FormatConverter-v8.2` 产物中的 APK。

## v8.1 剪辑入口与原声预览

- 导入视频自动打开剪辑窗口，不依赖主页输出格式；主页剪辑入口始终可用。
- 剪辑中可直接选择 H.264 / H.265 / AV1 MP4 导出，也可只保存编辑设置。
- 原声、背景音乐、音量与淡入淡出统一从剪辑窗口进入；取消剪辑会恢复本次声音设置。
- 保留 ImageView 画面预览，Media3 仅启用音频轨道，以音频位置驱动画面定位。
- 不支持的音轨、解码失败或准备超时会退回静音预览；切后台、失去音频焦点或拔耳机会暂停，关闭剪辑释放播放器。
- 混合导入时只剪辑和导出视频，其余文件仍保留在主页；没有视频时编辑首个 GIF。
- 预览同步播放素材原声与背景音乐；导出仍支持完整混音、循环、淡入淡出和 0–200% 音量。
- 之前工作流中的 Sonic / PDF 兼容修复已并入生成器；工作流监听其实际文件名。

本次验证：生成器和工作流语法检查、使用 Android 36 API 与实际依赖的 Java 17 源码编译通过。本地未运行 Android 真机/模拟器或完整 APK 打包；保留原 Actions 设备验证流程。下文性能与完整构建记录为 v8.0 的历史记录，不是 v8.1 新增测量。

## v8.0 原有改进

### 保留原功能，扩展至 37 项输出选项

JPEG、PNG、BMP、GIF、H.264/H.265/AV1 MP4、WebP 有损/无损、MP3、M4A、图片 PDF、ICO、TXT、HTML、CSV、JSON、YAML、XML、Markdown、TSV、VTT、SRT、文本 PDF 均保留。批量导出、ZIP、逐页 PDF 转图片、多尺寸 ICO、字幕和结构化文本转换也保留。

新增 DOCX、EPUB、ODT、WAV、RTF、TIFF、TGA、PPM、PGM、PBM、PAM、JSONL、FB2 输出，并扩展原格式之间的转换：

| 输入 | 新增/改进的输出 |
|---|---|
| TXT、Markdown、HTML、表格、结构化文本、字幕 | 可选择文字的 A4 PDF、DOCX、EPUB、ODT、RTF |
| 有文字层的 PDF | TXT、HTML、Markdown、DOCX、EPUB、ODT、RTF |
| DOCX、EPUB、ODT、RTF、FB2 | TXT、HTML、Markdown、PDF 及正文文档输出 |
| TIFF、TGA、PNM/PAM、静态 SVG/SVGZ | JPEG、PNG、WebP、BMP、TIFF、TGA、PPM、PGM、PBM、PAM、图片 PDF、ICO；多图可合成 GIF |
| JSONL / NDJSON | JSON、CSV、TSV、YAML、XML、Markdown、HTML、TXT 等原有结构化转换 |
| JSON、CSV、TSV、YAML、XML、Markdown 表格、字幕 | JSONL（每行一条 JSON） |
| 文本与正文文档 | FB2 电子书 |
| 多个 PDF | 按列表顺序合并为一个 PDF |
| 系统可解码的独立音频或视频 | MP3、M4A、WAV |
| 视频 / 多个视频 | 保留剪辑的 MP4、拼接、原声和背景音乐 |

文档转换提取正文，不承诺保留复杂版式、插图、公式或交互表单。EPUB 按 spine 阅读顺序提取。RTF 支持读取 Unicode 和常见 ANSI 代码页。扫描 PDF 不包含 OCR；加密且需要密码的 PDF 需先解锁。PDF 转结构化 CSV 不会猜测表格结构。

图片限制：TIFF 读取第一页，支持 8 bit 灰度/RGB/RGBA 和未压缩、Deflate、PackBits、LZW 条带，不支持 CMYK、瓦片、JPEG 压缩、BigTIFF。TGA 支持真彩色/灰度及 RLE。PNM 支持 P1–P7、最高 16 bit 输入（转换到 8 bit）。TIFF/TGA/PAM 输出保留透明；PPM/PGM/PBM 遇透明背景填白，PGM 转灰度，PBM 按 128 阈值转黑白。SVG/SVGZ 仅导入静态矢量，拒绝脚本、外部资源、滤镜、动画与 DTD，不提供伪矢量导出。HEIC/AVIF 等输入依赖系统解码器。

### 视频与音频

原有截取、变速、分割、删除、撤销/重做、旋转、裁切、镜像、亮度/对比度/饱和度、片段倒放和 GIF 循环均保留。新增：

- 视频剪辑、多视频拼接导出 MP4；GIF 转 MP4 可配乐。
- 原声 / 音乐独立 0–200% 音量，0% 静音。
- 音乐起点、音乐循环、首尾 0–10 秒淡入淡出。
- 裁切、删除、变速、倒放后的原声按片段处理；变速使用 Sonic 保持音调。
- 输入音轨由系统解码，多声道下混至双声道，统一重采样为 48 kHz。
- MP4 使用 AAC-LC 192 kbps，避免把不兼容原音轨直接塞进 MP4。M4A 对 AAC 保留极速原样提取，对其他可解码格式自动转码。
- WAV 输出 48 kHz / 16 bit / 双声道 PCM，约 11.52 MB/分钟。不能恢复原有有损压缩丢失的细节。
- 不支持的编码会报出错误，不会静默输出缺失的音轨。原声有问题时可设置原声音量 0%，仅配乐或静音导出。

剪辑预览使用兼容画面渲染并同步播放原声与背景音乐；删除片段会从时间轴折叠消失并可撤销。硬件编码、音频解码能力受手机影响。AV1 输出仍依赖 Android 14+ 与可用编码器。

### 推荐值和体验

推荐区域显示预计分辨率、质量数值、帧率、帧数上限、时长、自动码率等；批量显示首项信息。后台读取、250 ms 防抖，过期结果不会覆盖新选择。最终编码参数仍受设备和可用内存限制，导出进度显示实际值。

图片 PDF 显示实际 JPEG 质量。文本 PDF 不再显示无意义的 JPEG 质量滑块。音频显示采样率、位深或码率。导出中锁定声音设置。

### 性能、内存与稳定性

- 文本 PDF 改用矢量文字，不再为每页分配 1190×1684 的 ARGB 位图并压成 JPEG；去掉约 **7.64 MiB/页的临时位图**，文字更清晰且可复制。修正原先 22 px 测量对应 11 pt 布局导致过早换行的问题。
- 中文长行排版使用指数探测与二分查找，避免逐字反复测量整个候选行；保留代理对和组合字符。
- MP4 普通 drain 改为非阻塞轮询；仅结束排空时等待，移除每次空轮询最多 10 ms 的人为等待。
- 进度 UI 常规刷新从最多约 20 Hz 限制到 10 Hz，完成和开始立即刷新。
- 缩略图队列最多 32 项，转换前缩略图缓存缩至 1/4；低内存时缩小缓存。
- 预览按实际窗口和裁切需要解码，长边限制 960，不再固定以窗口的两倍宽高解码。保留缩放解码降级，不退回整张 4K/8K 帧。
- 修复预览关闭时主线程释放仍在解码中的 MediaMetadataRetriever 的竞争问题。
- 声音以固定块处理，长音轨和倒放使用有大小限制的磁盘缓存；正常视频按序流式编码，倒放只缓存相关片段。
- PDFBox 混合内存/磁盘缓存；文档压缩包、正文、页数、临时空间均有限制；XML 禁用 DTD/实体输入。
- 两个构建文件代替旧 Base64 压缩工程；修正构建触发路径，保留 Gradle 缓存、R8 和资源压缩，增加重复构建取消。

### 可复核的性能结果

桌面 JDK 17、26 万个中文字、11 pt 等宽模拟测量、5 次预热 / 11 次运行取中位数：旧排版约 **14.2 ms**，新排版约 **3.8 ms**，耗时减少约 **74%**；测量次数从 266,046 降到 42,323，减少约 **84%**。这是排版算法微基准，不是整个 APP、Android Paint 或手机的端到端性能提升。视频编码和整机内存变化没有真机基准，不宣称统一提升百分比。

## 本地构建

需要 JDK 17、Android SDK 36、Gradle 9.5.1、Python 与 Pillow：

```bash
python -m pip install Pillow==11.3.0
python android_project.py
gradle :app:testDebugUnitTest :app:assembleRelease
```

迁移旧生成目录或更换 SDK / Gradle 路径后，如遇重复 DEX 类错误，先执行 `gradle clean` 再构建。

生成目录不提交到仓库；修改 `android_project.py` 中的源文件字符串后重新生成。`--output` 可指定独立生成目录。

构建使用可安装的优化 Release 配置和开发签名。Actions 缓存开发签名以减少后续安装冲突；缓存清除或与原安装包签名不同仍可能需要卸载旧版。正式发行应使用妥善保管的稳定签名密钥。

## v8.0 历史验证记录

v8.0 已在全新生成目录、关闭构建缓存的条件下完成全部编译：25 项 JVM 测试通过，Release / Debug / 设备测试 APK 均构建成功，Release 验签及 16 KB ZIP 对齐通过。本地软件模拟器启动后未能完成设备测试，以下 7 项设备测试尚无本地通过记录；不能据此宣称所有手机音视频编码都已验证。

- 25 项 JVM 回归测试：TIFF 四种压缩、PNM/PAM/TGA 读取、采样与损坏数据、RTF 编码/往返，以及中文/emoji 换行、长词、页数限制、剪辑绝对时间、PCM 下混、倒放、混音限幅、非数值样本、DOCX/EPUB/RTF 输出。
- Release 编译、R8、资源压缩、APK 签名和 16 KB ZIP 对齐检查。
- Actions 在 API 28 / 35 模拟器执行 7 项设备测试：中文文字 PDF 提取、DOCX/EPUB/ODT 正文往返、WAV→AAC→WAV、视频配乐与截取/倒放/变速后导出、六种新增图片输出往返、SVG 渲染/外部资源拒绝、FB2/JSONL 往返。设备测试失败会阻止流程通过。

新增 PDFBox-Android、AndroidSVG 与 Media3 common/Sonic；v8.1 增加 Media3 ExoPlayer， 会增加安装包体积；没有打包体积很大的 FFmpeg 全套，也没有新增联网权限。
''',
    'app/build.gradle': r'''plugins {
    id 'com.android.application'
}

android {
    namespace 'com.qi.formatconverter'
    compileSdk 36

    defaultConfig {
        applicationId 'com.qi.formatconverter'
        minSdk 28
        targetSdk 36
        versionCode 21
        versionName '8.2'
        testInstrumentationRunner 'androidx.test.runner.AndroidJUnitRunner'
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            // The workflow distributes an installable optimized APK, so use Android's generated
            // debug key while keeping release/R8 optimizations enabled.
            signingConfig signingConfigs.debug
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    packaging {
        jniLibs {
            useLegacyPackaging = false
        }
        resources {
            excludes += ['/META-INF/{AL2.0,LGPL2.1}']
        }
    }
}

dependencies {
    implementation 'pl.droidsonroids.gif:android-gif-drawable:1.2.32'
    implementation 'androidx.recyclerview:recyclerview:1.4.0'
    implementation 'co.ntbl:lame:1.0.0'
    implementation 'com.caverock:androidsvg-aar:1.4'
    implementation 'com.tom-roush:pdfbox-android:2.0.27.0'
    implementation 'androidx.media3:media3-common:1.9.0'
    implementation 'androidx.media3:media3-exoplayer:1.9.0'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test:runner:1.6.2'
    androidTestImplementation 'androidx.test.ext:junit:1.2.1'
}
''',
    'app/proguard-rules.pro': r'''-keep class pl.droidsonroids.gif.** { *; }
-dontwarn javax.sound.sampled.**
-dontwarn java.beans.**

# PDFBox optional JPEG2000 image plugin is not used by text extraction or page merging.
-dontwarn com.gemalto.jp2.JP2Decoder
-dontwarn com.gemalto.jp2.JP2Encoder
''',
    'app/src/androidTest/java/com/qi/formatconverter/DeviceIntegrationTest.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.graphics.*;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;
import org.junit.Test;
import org.junit.runner.RunWith;
import static org.junit.Assert.*;
import java.io.*;
import java.nio.*;
import java.util.*;

@RunWith(AndroidJUnit4.class)
public class DeviceIntegrationTest {
    private Context context(){return InstrumentationRegistry.getInstrumentation().getTargetContext();}
    private File temp(String extension)throws IOException{return File.createTempFile("integration_",extension,context().getCacheDir());}
    @Test public void nativeTextPdfCanBeExtractedIncludingChinese() throws Exception {
        File file=temp(".pdf");PdfDocument pdf=new PdfDocument();
        try {
            PdfDocument.Page page=pdf.startPage(new PdfDocument.PageInfo.Builder(595,842,1).create());
            Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG);paint.setTextSize(18);
            page.getCanvas().drawText("Hello PDF 中文植物",50,80,paint);pdf.finishPage(page);
            try(FileOutputStream out=new FileOutputStream(file)){pdf.writeTo(out);}pdf.close();
            String text=DocumentKit.read(context(),Uri.fromFile(file),"PDF",()->{});
            assertTrue(text,text.contains("Hello PDF"));assertTrue(text,text.contains("中文植物"));
        } finally {file.delete();}
    }
    @Test public void officeAndEbookRoundTrip()throws Exception {
        int[] formats={24,25,26};String[] names={"DOCX","EPUB","ODT"};
        for(int i=0;i<formats.length;i++){
            File file=temp(".zip");try{DocumentKit.write(file,formats[i],"中文植物 🌱 & < >\nSecond line","标题",()->{});String text=DocumentKit.read(context(),Uri.fromFile(file),names[i],()->{});assertTrue(text,text.contains("中文植物 🌱 & < >"));assertTrue(text,text.contains("Second line"));}finally{file.delete();}
        }
    }
    private File wav()throws Exception {
        File pcm=temp(".pcm"),wav=temp(".wav");
        try(FileOutputStream out=new FileOutputStream(pcm)){
            ByteBuffer b=ByteBuffer.allocate(48000*2*4).order(ByteOrder.LITTLE_ENDIAN);
            for(int i=0;i<96000;i++){short v=(short)(Math.sin(i*2*Math.PI*440/48000)*9000);b.putShort(v).putShort(v);}out.write(b.array());
        }
        try{AudioPipeline.writeWav(pcm,wav,()->{});return wav;}finally{pcm.delete();}
    }
    @Test public void wavAacWavRoundTrip()throws Exception {
        File source=wav(),aac=temp(".m4a"),decoded=temp(".wav");
        try{
            AudioPipeline.convert(context(),Uri.fromFile(source),aac,false,()->{},(v,m)->{});
            assertTrue(AudioPipeline.isAac(context(),Uri.fromFile(aac)));
            AudioPipeline.convert(context(),Uri.fromFile(aac),decoded,true,()->{},(v,m)->{});
            assertTrue(decoded.length()>350000);assertTrue(decoded.length()<410000);
            try(RandomAccessFile in=new RandomAccessFile(decoded,"r")){in.seek(44+16000);byte[] b=new byte[10000];in.readFully(b);double energy=0;for(int i=0;i<b.length;i+=2){short sample=(short)((b[i]&255)|(b[i+1]<<8));energy+=sample*(double)sample;}assertTrue(energy>1e9);}
        }finally{source.delete();aac.delete();decoded.delete();}
    }
    @Test public void videoWithMusicCanBeTrimmedReversedAndSpeedChanged()throws Exception {
        File silent=temp(".mp4"),music=wav(),attached=null,edited=temp(".mp4"),result=null;
        try{
            Bitmap bitmap=Bitmap.createBitmap(320,180,Bitmap.Config.ARGB_8888);
            try(Mp4Encoder encoder=new Mp4Encoder(silent,320,180,24,500000,Mp4Encoder.MIME_H264,"H264")){
                for(int i=0;i<48;i++){bitmap.eraseColor(Color.rgb(i*5,70,100));encoder.encodeFrame(bitmap,i*1000000L/24);}encoder.finish();
            }finally{bitmap.recycle();}
            AudioPipeline.Settings settings=new AudioPipeline.Settings(Uri.fromFile(music),1,.5f,true,0,.1);
            attached=AudioPipeline.attach(context(),silent,Collections.emptyList(),1,settings,()->{},(v,m)->{});
            assertTrue(AudioPipeline.hasAudio(context(),Uri.fromFile(attached)));
            List<AudioPipeline.Segment> segments=Collections.singletonList(new AudioPipeline.Segment(Uri.fromFile(attached),250000,1750000,true,1.5));
            VideoExporter.export(context(),segments,AnimationEdits.NONE,edited,320,180,24,100,1,500000,Mp4Encoder.MIME_H264,"H264",()->{},(v,m)->{});
            result=AudioPipeline.attach(context(),edited,segments,1,new AudioPipeline.Settings(null,1,0,false,0,0),()->{},(v,m)->{});
            assertTrue(AudioPipeline.hasAudio(context(),Uri.fromFile(result)));
            long duration=VideoFrameDecoder.probe(context(),Uri.fromFile(result)).durationUs;
            assertTrue("duration="+duration,duration>850000&&duration<1150000);
        }finally{silent.delete();music.delete();edited.delete();if(attached!=null)attached.delete();if(result!=null)result.delete();}
    }

    @Test public void additionalRasterFormatsRoundTrip()throws Exception {
        Bitmap source=Bitmap.createBitmap(9,130,Bitmap.Config.ARGB_8888);source.eraseColor(Color.WHITE);source.setPixel(0,0,Color.BLACK);source.setPixel(8,129,Color.RED);
        try {for(int format=29;format<=34;format++){
            File file=temp(format==29?".tiff":format==30?".tga":format==34?".pam":format==33?".pbm":format==32?".pgm":".ppm");
            try {try(OutputStream out=new FileOutputStream(file)){ExtraImageFormats.write(source,format,out);}
                Bitmap decoded=ExtraImageFormats.decode(context(),Uri.fromFile(file),format==29?"TIFF":format==30?"TGA":"PNM",1000,1000,100000);
                try {assertEquals(9,decoded.getWidth());assertEquals(130,decoded.getHeight());assertEquals(Color.BLACK,decoded.getPixel(0,0));assertEquals(Color.WHITE,decoded.getPixel(1,0));if(format!=32&&format!=33)assertEquals(Color.RED,decoded.getPixel(8,129));}finally{decoded.recycle();}
            }finally{file.delete();}
        }}finally{source.recycle();}
        Bitmap alpha=Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888);alpha.setPixel(0,0,0x800000ff);
        try{for(int format:new int[]{29,30,34}){ByteArrayOutputStream out=new ByteArrayOutputStream();ExtraImageFormats.write(alpha,format,out);File file=temp(".image");try{try(OutputStream f=new FileOutputStream(file)){f.write(out.toByteArray());}Bitmap decoded=ExtraImageFormats.decode(context(),Uri.fromFile(file),format==29?"TIFF":format==30?"TGA":"PNM",10,10,100);try{assertEquals(0x800000ff,decoded.getPixel(0,0));}finally{decoded.recycle();}}finally{file.delete();}}}finally{alpha.recycle();}
    }
    @Test public void svgRendersAndRejectsExternalImage()throws Exception {
        File f=temp(".svg");try {
            try(OutputStream out=new FileOutputStream(f)){out.write("<svg xmlns='http://www.w3.org/2000/svg' width='16' height='8'><rect width='16' height='8' fill='#ff0000'/></svg>".getBytes(java.nio.charset.StandardCharsets.UTF_8));}
            Bitmap bitmap=ExtraImageFormats.decode(context(),Uri.fromFile(f),"SVG",100,100,10000);try{assertEquals(16,bitmap.getWidth());assertEquals(Color.RED,bitmap.getPixel(4,4));}finally{bitmap.recycle();}
            try(OutputStream out=new FileOutputStream(f)){out.write("<svg><image href='https://example.com/private'/></svg>".getBytes(java.nio.charset.StandardCharsets.UTF_8));}
            try{ExtraImageFormats.decode(context(),Uri.fromFile(f),"SVG",100,100,10000);fail();}catch(IOException expected){}
        }finally{f.delete();}
    }
    @Test public void fb2AndJsonlRoundTrip()throws Exception {
        String source="中文 🌱 & < >\nSecond line";assertEquals(source,ExtraTextFormats.fb2Text(ExtraTextFormats.fb2(source,"标题")));
        String jsonl="{\"name\":\"中文\",\"n\":1}\n[1,true,null]\n\"text\"\n";
        assertEquals(jsonl,ExtraTextFormats.jsonToJsonl(ExtraTextFormats.jsonlToJson(jsonl)));
        try{ExtraTextFormats.jsonlToJson("{\"n\":1} garbage");fail();}catch(IOException expected){}
    }
}
''',
    'app/src/main/AndroidManifest.xml': r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="格式转换器"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity
            android:name=".MainActivity"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:launchMode="singleTop"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="image/*" />
                <data android:mimeType="video/*" />
                <data android:mimeType="audio/*" />
                <data android:mimeType="application/epub+zip" />
                <data android:mimeType="application/vnd.oasis.opendocument.text" />
                <data android:mimeType="application/rtf" />
                <data android:mimeType="application/x-ndjson" />
                <data android:mimeType="application/x-fictionbook+xml" />
                <data android:mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document" />
                <data android:mimeType="application/pdf" />
                <data android:mimeType="text/*" />
                <data android:mimeType="application/json" />
                <data android:mimeType="application/yaml" />
                <data android:mimeType="application/x-yaml" />
                <data android:mimeType="application/xml" />
                <data android:mimeType="application/x-subrip" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND_MULTIPLE" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="image/*" />
                <data android:mimeType="video/*" />
                <data android:mimeType="audio/*" />
                <data android:mimeType="application/epub+zip" />
                <data android:mimeType="application/vnd.oasis.opendocument.text" />
                <data android:mimeType="application/rtf" />
                <data android:mimeType="application/x-ndjson" />
                <data android:mimeType="application/x-fictionbook+xml" />
                <data android:mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document" />
                <data android:mimeType="application/pdf" />
                <data android:mimeType="text/*" />
                <data android:mimeType="application/json" />
                <data android:mimeType="application/yaml" />
                <data android:mimeType="application/x-yaml" />
                <data android:mimeType="application/xml" />
                <data android:mimeType="application/x-subrip" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''',
    'app/src/main/assets/THIRD_PARTY_NOTICES.txt': r'''Format Converter third-party notices

Java LAME 1.0.0 (co.ntbl:lame)
Native Java port of LAME, maintained by daberkow.
Licensed under GNU Lesser General Public License v3.0.
Source: https://github.com/daberkow/java-lame
License: https://www.gnu.org/licenses/lgpl-3.0.html

android-gif-drawable 1.2.32
Copyright 2013-present Karol Wrótniak and contributors.
Licensed under the MIT License.
Source: https://github.com/koral--/android-gif-drawable

AndroidX RecyclerView
Copyright The Android Open Source Project.
Licensed under the Apache License 2.0.
Source: https://developer.android.com/jetpack/androidx

PDFBox-Android 2.0.27.0 / Apache PDFBox — Apache-2.0
https://github.com/TomRoush/PdfBox-Android
Jetpack Media3 common 1.9.0 (Sonic speed/pitch/resampling) — Apache-2.0
https://github.com/androidx/media
Document text extraction does not include OCR.

AndroidSVG 1.4 — Apache License 2.0
Copyright Paul LeBeau and contributors.
https://github.com/BigBadaboom/androidsvg
''',
    'app/src/main/java/com/qi/formatconverter/AnimationEdits.java': r'''package com.qi.formatconverter;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/** Immutable edit settings shared by image, GIF and video animation pipelines. */
final class AnimationEdits {
    static final int CROP_NONE = 0;
    static final int CROP_SQUARE = 1;
    static final int CROP_4_3 = 2;
    static final int CROP_3_4 = 3;
    static final int CROP_16_9 = 4;
    static final int CROP_9_16 = 5;

    static final AnimationEdits NONE = new AnimationEdits(
            0.0, 0.0, 1.0, CROP_NONE, 0,
            false, false, 0, 100, 100,
            Collections.emptyList(), Collections.emptyList());

    final double trimStartSeconds;
    final double trimDurationSeconds;
    final double speed;
    final int cropMode;
    final int rotationDegrees;
    final boolean flipHorizontal;
    final boolean flipVertical;
    final int brightness;
    final int contrast;
    final int saturation;
    final List<TimeRange> deletedRanges;
    final List<TimeRange> reversedRanges;

    AnimationEdits(
            double trimStartSeconds,
            double trimDurationSeconds,
            double speed,
            int cropMode,
            int rotationDegrees,
            boolean flipHorizontal,
            boolean flipVertical,
            int brightness,
            int contrast,
            int saturation) {
        this(trimStartSeconds, trimDurationSeconds, speed, cropMode, rotationDegrees,
                flipHorizontal, flipVertical, brightness, contrast, saturation,
                Collections.emptyList(), Collections.emptyList());
    }

    AnimationEdits(
            double trimStartSeconds,
            double trimDurationSeconds,
            double speed,
            int cropMode,
            int rotationDegrees,
            boolean flipHorizontal,
            boolean flipVertical,
            int brightness,
            int contrast,
            int saturation,
            List<TimeRange> deletedRanges) {
        this(trimStartSeconds, trimDurationSeconds, speed, cropMode, rotationDegrees,
                flipHorizontal, flipVertical, brightness, contrast, saturation,
                deletedRanges, Collections.emptyList());
    }

    AnimationEdits(
            double trimStartSeconds,
            double trimDurationSeconds,
            double speed,
            int cropMode,
            int rotationDegrees,
            boolean flipHorizontal,
            boolean flipVertical,
            int brightness,
            int contrast,
            int saturation,
            List<TimeRange> deletedRanges,
            List<TimeRange> reversedRanges) {
        this.trimStartSeconds = clampFinite(trimStartSeconds, 0.0, 86_400.0, 0.0);
        this.trimDurationSeconds = clampFinite(trimDurationSeconds, 0.0, 86_400.0, 0.0);
        this.speed = clampFinite(speed, 0.25, 4.0, 1.0);
        this.cropMode = cropMode >= CROP_NONE && cropMode <= CROP_9_16
                ? cropMode : CROP_NONE;
        this.rotationDegrees = normalizeRotation(rotationDegrees);
        this.flipHorizontal = flipHorizontal;
        this.flipVertical = flipVertical;
        this.brightness = clamp(brightness, -50, 50);
        this.contrast = clamp(contrast, 50, 150);
        this.saturation = clamp(saturation, 0, 200);
        this.deletedRanges = normalizeRanges(deletedRanges);
        this.reversedRanges = normalizeRanges(reversedRanges);
    }

    boolean hasVisualEdits() {
        return cropMode != CROP_NONE
                || rotationDegrees != 0
                || flipHorizontal
                || flipVertical
                || brightness != 0
                || contrast != 100
                || saturation != 100;
    }

    boolean hasTimelineEdits() {
        return trimStartSeconds > 0.0
                || trimDurationSeconds > 0.0
                || !deletedRanges.isEmpty()
                || !reversedRanges.isEmpty()
                || Math.abs(speed - 1.0) > 0.0001;
    }

    double cropAspect() {
        switch (cropMode) {
            case CROP_SQUARE: return 1.0;
            case CROP_4_3: return 4.0 / 3.0;
            case CROP_3_4: return 3.0 / 4.0;
            case CROP_16_9: return 16.0 / 9.0;
            case CROP_9_16: return 9.0 / 16.0;
            default: return 0.0;
        }
    }

    List<TimeRange> keptRanges(double durationSeconds) {
        return keptRanges(0.0, durationSeconds);
    }

    /**
     * Returns the parts of an absolute source-time window that remain after split/delete edits.
     * Keeping the ranges in source time makes a cut selected in the preview stay correct when a
     * non-zero trim start is also used.
     */
    List<TimeRange> keptRanges(double windowStartSeconds, double windowEndSeconds) {
        double start = clampFinite(windowStartSeconds, 0.0, 86_400.0, 0.0);
        double end = clampFinite(windowEndSeconds, start, 86_400.0, start);
        if (end - start <= 0.0) return Collections.emptyList();
        List<TimeRange> kept = new ArrayList<>();
        double cursor = start;
        for (TimeRange deleted : deletedRanges) {
            double cutStart = Math.max(start, Math.min(end, deleted.startSeconds));
            double cutEnd = Math.max(cutStart, Math.min(end, deleted.endSeconds));
            if (cutStart > cursor + 0.0005) {
                kept.add(new TimeRange(cursor, cutStart));
            }
            cursor = Math.max(cursor, cutEnd);
            if (cursor >= end) break;
        }
        if (cursor < end - 0.0005) kept.add(new TimeRange(cursor, end));
        return kept;
    }

    double keptDurationSeconds(double durationSeconds) {
        return keptDurationSeconds(0.0, durationSeconds);
    }

    double keptDurationSeconds(double windowStartSeconds, double windowEndSeconds) {
        double total = 0.0;
        for (TimeRange range : keptRanges(windowStartSeconds, windowEndSeconds)) {
            total += range.durationSeconds();
        }
        return total;
    }

    double sourceSecondAtKeptOffset(double durationSeconds, double keptOffsetSeconds) {
        return sourceSecondAtKeptOffset(0.0, durationSeconds, keptOffsetSeconds);
    }

    double sourceSecondAtKeptOffset(
            double windowStartSeconds, double windowEndSeconds,
            double keptOffsetSeconds) {
        List<PlaybackRange> playback = playbackRanges(windowStartSeconds, windowEndSeconds);
        if (playback.isEmpty()) return Math.max(0.0, windowStartSeconds);
        double remaining = Math.max(0.0, keptOffsetSeconds);
        for (PlaybackRange range : playback) {
            double length = range.durationSeconds();
            if (remaining < length) {
                if (range.reversed) {
                    return Math.max(range.startSeconds,
                            range.endSeconds - remaining - 0.001);
                }
                return range.startSeconds + remaining;
            }
            remaining -= length;
        }
        PlaybackRange last = playback.get(playback.size() - 1);
        return last.reversed
                ? last.startSeconds
                : Math.max(last.startSeconds, last.endSeconds - 0.001);
    }

    List<PlaybackRange> playbackRanges(double windowStartSeconds, double windowEndSeconds) {
        List<TimeRange> kept = keptRanges(windowStartSeconds, windowEndSeconds);
        if (kept.isEmpty()) return Collections.emptyList();
        List<PlaybackRange> result = new ArrayList<>();
        for (TimeRange keep : kept) {
            List<Double> boundaries = new ArrayList<>();
            boundaries.add(keep.startSeconds);
            boundaries.add(keep.endSeconds);
            for (TimeRange reversed : reversedRanges) {
                double start = Math.max(keep.startSeconds, reversed.startSeconds);
                double end = Math.min(keep.endSeconds, reversed.endSeconds);
                if (end - start <= 0.0005) continue;
                boundaries.add(start);
                boundaries.add(end);
            }
            Collections.sort(boundaries);
            for (int i = 0; i + 1 < boundaries.size(); i++) {
                double start = boundaries.get(i);
                double end = boundaries.get(i + 1);
                if (end - start <= 0.0005) continue;
                double midpoint = start + (end - start) * 0.5;
                result.add(new PlaybackRange(
                        start, end, isInside(midpoint, reversedRanges)));
            }
        }
        return Collections.unmodifiableList(result);
    }

    private static boolean isInside(double second, List<TimeRange> ranges) {
        for (TimeRange range : ranges) {
            if (second >= range.startSeconds && second < range.endSeconds) return true;
        }
        return false;
    }

    private static List<TimeRange> normalizeRanges(List<TimeRange> values) {
        if (values == null || values.isEmpty()) return Collections.emptyList();
        List<TimeRange> sorted = new ArrayList<>();
        for (TimeRange value : values) {
            if (value == null) continue;
            double start = clampFinite(value.startSeconds, 0.0, 86_400.0, 0.0);
            double end = clampFinite(value.endSeconds, 0.0, 86_400.0, 0.0);
            if (end < start) {
                double swap = start;
                start = end;
                end = swap;
            }
            if (end - start >= 0.001) sorted.add(new TimeRange(start, end));
        }
        if (sorted.isEmpty()) return Collections.emptyList();
        sorted.sort(Comparator.comparingDouble(range -> range.startSeconds));
        List<TimeRange> merged = new ArrayList<>();
        for (TimeRange value : sorted) {
            if (merged.isEmpty()) {
                merged.add(value);
                continue;
            }
            TimeRange previous = merged.get(merged.size() - 1);
            if (value.startSeconds <= previous.endSeconds + 0.001) {
                merged.set(merged.size() - 1,
                        new TimeRange(previous.startSeconds,
                                Math.max(previous.endSeconds, value.endSeconds)));
            } else {
                merged.add(value);
            }
        }
        return Collections.unmodifiableList(merged);
    }

    static final class PlaybackRange {
        final double startSeconds;
        final double endSeconds;
        final boolean reversed;

        PlaybackRange(double startSeconds, double endSeconds, boolean reversed) {
            this.startSeconds = startSeconds;
            this.endSeconds = endSeconds;
            this.reversed = reversed;
        }

        double durationSeconds() {
            return Math.max(0.0, endSeconds - startSeconds);
        }
    }

    static final class TimeRange {
        final double startSeconds;
        final double endSeconds;

        TimeRange(double startSeconds, double endSeconds) {
            this.startSeconds = startSeconds;
            this.endSeconds = endSeconds;
        }

        double durationSeconds() {
            return Math.max(0.0, endSeconds - startSeconds);
        }
    }

    private static int normalizeRotation(int value) {
        int normalized = ((value % 360) + 360) % 360;
        int quarterTurns = Math.round(normalized / 90f) & 3;
        return quarterTurns * 90;
    }

    private static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }

    private static double clampFinite(
            double value, double min, double max, double fallback) {
        if (Double.isNaN(value) || Double.isInfinite(value)) return fallback;
        return Math.max(min, Math.min(max, value));
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/AudioConverter.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.media.MediaCodec;
import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import android.net.Uri;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;

/** Streaming video-audio extraction with platform decode and pure-Java MP3 encode. */
final class AudioConverter {
    private static final long CODEC_STALL_TIMEOUT_NS = 15_000_000_000L;

    interface CancelCheck {
        boolean isCancelled();
    }

    interface ProgressCallback {
        void onProgress(int perMille, String message);
    }

    private AudioConverter() { }

    static long estimateOutputBytes(Context context, Uri uri, boolean mp3) {
        try (AssetFileDescriptor afd = context.getContentResolver()
                .openAssetFileDescriptor(uri, "r")) {
            if (afd == null) return 16L * 1024 * 1024;
            MediaExtractor extractor = new MediaExtractor();
            try {
                setDataSource(extractor, afd);
                int track = findAudioTrack(extractor);
                if (track < 0) return 16L * 1024 * 1024;
                MediaFormat format = extractor.getTrackFormat(track);
                long durationUs = Math.max(0L,
                        getLong(format, MediaFormat.KEY_DURATION, 0L));
                int channels = Math.max(1,
                        getInt(format, MediaFormat.KEY_CHANNEL_COUNT, 2));
                long bitrate = mp3
                        ? (channels == 1 ? 128_000L : 192_000L)
                        : Math.max(8_000L, Math.min(2_000_000L,
                                getInt(format, MediaFormat.KEY_BIT_RATE, 256_000)));
                long payload = durationUs <= 0
                        ? 8L * 1024 * 1024
                        : (long) Math.ceil(durationUs / 1_000_000.0 * bitrate / 8.0);
                return Math.max(8L * 1024 * 1024,
                        Math.min(Long.MAX_VALUE - 2L * 1024 * 1024,
                                payload) + 2L * 1024 * 1024);
            } finally {
                extractor.release();
            }
        } catch (Exception ignored) {
            return 16L * 1024 * 1024;
        }
    }

    static void videoToMp3(
            Context context, Uri uri, File output,
            CancelCheck cancelCheck, ProgressCallback progress) throws Exception {
        try (AssetFileDescriptor afd = context.getContentResolver()
                     .openAssetFileDescriptor(uri, "r");
             OutputStream stream = new BufferedOutputStream(
                     new FileOutputStream(output), 256 * 1024)) {
            if (afd == null) throw new IOException("无法打开视频文件");
            MediaExtractor extractor = new MediaExtractor();
            MediaCodec decoder = null;
            PureJavaMp3Encoder mp3 = null;
            try {
                setDataSource(extractor, afd);
                int track = findAudioTrack(extractor);
                if (track < 0) throw new IOException("视频中没有音轨");
                extractor.selectTrack(track);
                MediaFormat inputFormat = extractor.getTrackFormat(track);
                String mime = inputFormat.getString(MediaFormat.KEY_MIME);
                if (mime == null) throw new IOException("无法识别视频音频编码");
                long durationUs = getLong(inputFormat, MediaFormat.KEY_DURATION, 0L);

                decoder = MediaCodec.createDecoderByType(mime);
                decoder.configure(inputFormat, null, null, 0);
                decoder.start();

                boolean inputEos = false;
                boolean outputEos = false;
                MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
                long lastProgressNs = System.nanoTime();
                while (!outputEos) {
                    checkCancelled(cancelCheck);
                    if (!inputEos) {
                        int inputIndex = decoder.dequeueInputBuffer(8_000);
                        if (inputIndex >= 0) {
                            ByteBuffer input = decoder.getInputBuffer(inputIndex);
                            if (input == null) {
                                decoder.queueInputBuffer(inputIndex, 0, 0, 0,
                                        MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                                inputEos = true;
                            } else {
                                input.clear();
                                int size = extractor.readSampleData(input, 0);
                                if (size < 0) {
                                    decoder.queueInputBuffer(inputIndex, 0, 0, 0,
                                            MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                                    inputEos = true;
                                } else {
                                    long ptsUs = Math.max(0L, extractor.getSampleTime());
                                    decoder.queueInputBuffer(inputIndex, 0, size, ptsUs, 0);
                                    extractor.advance();
                                }
                            }
                            lastProgressNs = System.nanoTime();
                        }
                    }

                    int outputIndex = decoder.dequeueOutputBuffer(info, 8_000);
                    if (outputIndex == MediaCodec.INFO_TRY_AGAIN_LATER) {
                        if (System.nanoTime() - lastProgressNs > CODEC_STALL_TIMEOUT_NS) {
                            throw new IOException("系统音频解码器超过 15 秒没有进展");
                        }
                        continue;
                    }
                    if (outputIndex == MediaCodec.INFO_OUTPUT_FORMAT_CHANGED) {
                        lastProgressNs = System.nanoTime();
                        continue;
                    }
                    if (outputIndex < 0) continue;
                    lastProgressNs = System.nanoTime();

                    try {
                        if (info.size > 0) {
                            MediaFormat outputFormat = decoder.getOutputFormat(outputIndex);
                            if (mp3 == null) {
                                int sampleRate = getInt(
                                        outputFormat, MediaFormat.KEY_SAMPLE_RATE,
                                        getInt(inputFormat, MediaFormat.KEY_SAMPLE_RATE, 44_100));
                                int channels = getInt(
                                        outputFormat, MediaFormat.KEY_CHANNEL_COUNT,
                                        getInt(inputFormat, MediaFormat.KEY_CHANNEL_COUNT, 2));
                                int pcmEncoding = getInt(
                                        outputFormat, MediaFormat.KEY_PCM_ENCODING,
                                        PureJavaMp3Encoder.PCM_16_BIT);
                                int channelMask = getInt(
                                        outputFormat, MediaFormat.KEY_CHANNEL_MASK, 0);
                                mp3 = new PureJavaMp3Encoder(
                                        stream, sampleRate, channels, pcmEncoding,
                                        channelMask);
                            }
                            ByteBuffer decoded = decoder.getOutputBuffer(outputIndex);
                            if (decoded != null) {
                                ByteBuffer slice = decoded.duplicate();
                                slice.position(info.offset);
                                slice.limit(info.offset + info.size);
                                mp3.writePcm(slice.slice());
                            }
                            int value = durationUs > 0
                                    ? (int) Math.min(990L,
                                            info.presentationTimeUs * 990L / durationUs)
                                    : 0;
                            if (progress != null) {
                                progress.onProgress(value,
                                        "正在提取并编码 MP3：" + (value / 10) + "%");
                            }
                        }
                        outputEos = (info.flags & MediaCodec.BUFFER_FLAG_END_OF_STREAM) != 0;
                    } finally {
                        decoder.releaseOutputBuffer(outputIndex, false);
                    }
                }
                if (mp3 == null) throw new IOException("没有解码到可用音频");
                checkCancelled(cancelCheck);
                mp3.finish();
                if (mp3.writtenBytes() <= 0) throw new IOException("MP3 输出为空");
                if (progress != null) progress.onProgress(1000, "MP3 转换完成");
            } finally {
                if (mp3 != null) mp3.close();
                if (decoder != null) {
                    try { decoder.stop(); } catch (Exception ignored) { }
                    try { decoder.release(); } catch (Exception ignored) { }
                }
                extractor.release();
            }
        }
    }

    static void videoToM4a(
            Context context, Uri uri, File output,
            CancelCheck cancelCheck, ProgressCallback progress) throws Exception {
        try (AssetFileDescriptor afd = context.getContentResolver()
                .openAssetFileDescriptor(uri, "r")) {
            if (afd == null) throw new IOException("无法打开视频文件");
            MediaExtractor extractor = new MediaExtractor();
            MediaMuxer muxer = null;
            boolean muxerStarted = false;
            try {
                setDataSource(extractor, afd);
                int sourceTrack = findAudioTrack(extractor);
                if (sourceTrack < 0) throw new IOException("视频中没有音轨");
                MediaFormat format = extractor.getTrackFormat(sourceTrack);
                String mime = format.getString(MediaFormat.KEY_MIME);
                if (!"audio/mp4a-latm".equals(mime) && !"audio/aac".equals(mime)) {
                    throw new IOException("原音轨不是 AAC，请改用 MP3 输出");
                }
                long durationUs = getLong(format, MediaFormat.KEY_DURATION, 0L);
                extractor.selectTrack(sourceTrack);
                muxer = new MediaMuxer(
                        output.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
                int destinationTrack = muxer.addTrack(format);
                muxer.start();
                muxerStarted = true;

                int maxInputSize = Math.max(64 * 1024,
                        Math.min(4 * 1024 * 1024,
                                getInt(format, MediaFormat.KEY_MAX_INPUT_SIZE, 512 * 1024)));
                ByteBuffer buffer = ByteBuffer.allocateDirect(maxInputSize);
                MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
                long firstPtsUs = -1L;
                int sampleCount = 0;
                while (true) {
                    checkCancelled(cancelCheck);
                    buffer.clear();
                    int size = extractor.readSampleData(buffer, 0);
                    if (size < 0) break;
                    long ptsUs = Math.max(0L, extractor.getSampleTime());
                    if (firstPtsUs < 0) firstPtsUs = ptsUs;
                    info.set(0, size, Math.max(0L, ptsUs - firstPtsUs),
                            extractor.getSampleFlags());
                    buffer.position(0);
                    buffer.limit(size);
                    muxer.writeSampleData(destinationTrack, buffer, info);
                    sampleCount++;
                    int value = durationUs > 0
                            ? (int) Math.min(999L, ptsUs * 1000L / durationUs)
                            : 0;
                    if (progress != null) {
                        progress.onProgress(value,
                                "正在无损提取 M4A：" + (value / 10) + "%");
                    }
                    extractor.advance();
                }
                if (sampleCount == 0) throw new IOException("AAC 音轨为空");
                checkCancelled(cancelCheck);
                if (progress != null) progress.onProgress(1000, "M4A 提取完成");
            } finally {
                if (muxer != null) {
                    if (muxerStarted) {
                        try { muxer.stop(); } catch (Exception ignored) { }
                    }
                    try { muxer.release(); } catch (Exception ignored) { }
                }
                extractor.release();
            }
        }
    }

    private static int findAudioTrack(MediaExtractor extractor) {
        for (int i = 0; i < extractor.getTrackCount(); i++) {
            MediaFormat format = extractor.getTrackFormat(i);
            String mime = format.getString(MediaFormat.KEY_MIME);
            if (mime != null && mime.startsWith("audio/")) return i;
        }
        return -1;
    }

    private static void setDataSource(MediaExtractor extractor, AssetFileDescriptor afd)
            throws IOException {
        long length = afd.getLength();
        if (length >= 0) {
            extractor.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), length);
        } else {
            extractor.setDataSource(afd.getFileDescriptor());
        }
    }

    private static int getInt(MediaFormat format, String key, int fallback) {
        try { return format.containsKey(key) ? format.getInteger(key) : fallback; }
        catch (Exception ignored) { return fallback; }
    }

    private static long getLong(MediaFormat format, String key, long fallback) {
        try { return format.containsKey(key) ? format.getLong(key) : fallback; }
        catch (Exception ignored) { return fallback; }
    }

    private static void checkCancelled(CancelCheck check) throws InterruptedIOException {
        if (Thread.currentThread().isInterrupted()
                || (check != null && check.isCancelled())) {
            throw new InterruptedIOException("转换已取消");
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/AudioPipeline.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.net.Uri;
import android.media.*;
import androidx.media3.common.audio.AudioProcessor;
import androidx.media3.common.audio.SonicAudioProcessor;
import java.io.*;
import java.nio.*;
import java.util.*;

/** Platform decoders -> 48 kHz stereo PCM on disk -> mix -> AAC/WAV. RAM stays bounded. */
final class AudioPipeline {
    static final int RATE=48000;
    static final int FRAME_BYTES=4;
    static final long MAX_PCM_BYTES=2L*1024*1024*1024;
    interface Check { void check() throws Exception; }
    interface Progress { void update(int value,String message); }
    static final class Settings {
        final Uri music;
        final float originalVolume,musicVolume;
        final boolean loopMusic;
        final double musicStart,fade;
        Settings(Uri music,float originalVolume,float musicVolume,boolean loopMusic,double musicStart,double fade) {
            this.music=music;this.originalVolume=originalVolume;this.musicVolume=musicVolume;
            this.loopMusic=loopMusic;this.musicStart=musicStart;this.fade=fade;
        }
    }
    static final class Segment {
        final Uri uri;final long startUs,endUs;final boolean reverse;final double speed;
        Segment(Uri uri,long startUs,long endUs,boolean reverse,double speed){this.uri=uri;this.startUs=startUs;this.endUs=endUs;this.reverse=reverse;this.speed=speed;}
        long frames(){return Math.max(1,Math.round((endUs-startUs)/1e6/speed*RATE));}
    }
    private AudioPipeline(){ }
    static boolean hasAudio(Context c,Uri uri) throws IOException {
        MediaExtractor e=new MediaExtractor();try{e.setDataSource(c,uri,null);return audioTrack(e)>=0;}finally{e.release();}
    }
    static boolean isAac(Context c,Uri uri) throws IOException {
        MediaExtractor e=new MediaExtractor();try{e.setDataSource(c,uri,null);int t=audioTrack(e);return t>=0&&"audio/mp4a-latm".equals(e.getTrackFormat(t).getString(MediaFormat.KEY_MIME));}finally{e.release();}
    }
    static long duration(Context c,Uri uri) throws IOException {
        MediaExtractor e=new MediaExtractor();try{e.setDataSource(c,uri,null);int t=audioTrack(e);if(t<0)throw new IOException("文件没有音轨");MediaFormat f=e.getTrackFormat(t);return f.containsKey(MediaFormat.KEY_DURATION)?f.getLong(MediaFormat.KEY_DURATION):0;}finally{e.release();}
    }
    static void convert(Context c,Uri uri,File output,boolean wav,Check check,Progress progress) throws Exception {
        File pcm=temp(c,".pcm");
        try {
            long duration=duration(c,uri);
            ensureSpace(c,duration>0?Math.min(MAX_PCM_BYTES,Math.round(duration/1e6*RATE)*8):64L*1024*1024);
            decode(c,uri,0,duration>0?duration:Long.MAX_VALUE,pcm,false,check);
            if(pcm.length()==0)throw new IOException("没有解码到音频");
            if(wav)writeWav(pcm,output,check);else encodeAac(pcm,output,check,progress);
        } finally {pcm.delete();}
    }
    static File attach(Context c,File video,List<Segment> segments,int loops,Settings settings,Check check,Progress progress) throws Exception {
        long durationUs=videoDuration(video);
        long targetFrames=Math.max(1,Math.round(durationUs/1e6*RATE));
        if(targetFrames*4>MAX_PCM_BYTES)throw new IOException("音频超过约 3 小时的处理上限，请分段导出");
        boolean originals=false;
        if(settings.originalVolume>0)for(Segment segment:segments)if(hasAudio(c,segment.uri)){originals=true;break;}
        if(!originals&&(settings.music==null||settings.musicVolume<=0))return video;
        long originalFrames=0;
        for(Segment s:segments)originalFrames+=s.frames();
        if(originalFrames*4>MAX_PCM_BYTES)throw new IOException("原声音轨过长，请分段导出");
        ensureSpace(c,Math.min(MAX_PCM_BYTES,Math.max(targetFrames,originalFrames)*12)+video.length());
        List<File> temporary=new ArrayList<>();
        File original=temp(c,".pcm");temporary.add(original);
        File music=temp(c,".pcm");temporary.add(music);
        File mixed=temp(c,".pcm");temporary.add(mixed);
        File audio=temp(c,".m4a");temporary.add(audio);
        File result=temp(c,".mp4");boolean success=false;
        try {
            if(originals) {
                try(OutputStream out=new BufferedOutputStream(new FileOutputStream(original),65536)) {
                    for(int i=0;i<segments.size();i++) {
                        check.check();
                        ensureSpace(c,2L*1024*1024);Segment s=segments.get(i);
                        progress.update(10+(int)(220L*i/Math.max(1,segments.size())),"准备原声片段 "+(i+1)+" / "+segments.size());
                        File raw=temp(c,".pcm");File edited=temp(c,".pcm");
                        try {
                            decode(c,s.uri,s.startUs,s.endUs,raw,true,check);
                            // Pad before reversal so a short/late source track keeps its sync.
                            long expectedBytes=Math.max(1,Math.round((s.endUs-s.startUs)/1e6*RATE))*4;
                            if(expectedBytes>MAX_PCM_BYTES)throw new IOException("音频片段过长，请分段处理");
                            try(RandomAccessFile padded=new RandomAccessFile(raw,"rw")){padded.setLength(expectedBytes);}
                            speed(raw,edited,s.reverse,s.speed,check);
                            copyExact(edited,out,s.frames()*4,check);
                        } finally {raw.delete();edited.delete();}
                    }
                }
            }
            if(settings.music!=null&&settings.musicVolume>0) {
                long start=Math.round(settings.musicStart*1e6);
                decode(c,settings.music,start,start+durationUs,music,false,check);
                if(music.length()==0)throw new IOException("背景音乐起点之后没有可用声音");
            }
            try(RandomAccessFile a=new RandomAccessFile(original,"r");RandomAccessFile b=new RandomAccessFile(music,"r");OutputStream out=new BufferedOutputStream(new FileOutputStream(mixed),65536)) {
                byte[] x=new byte[32768],y=new byte[32768];long done=0;
                while(done<targetFrames) {
                    check.check();int bytes=(int)Math.min(x.length,(targetFrames-done)*4);
                    readLoop(a,x,bytes,originals&&loops>1);
                    readLoop(b,y,bytes,settings.loopMusic);
                    PcmMath.mix(x,y,bytes,settings.originalVolume,settings.musicVolume,done,targetFrames,Math.round(settings.fade*RATE));
                    out.write(x,0,bytes);done+=bytes/4;
                    if((done&65535)<8192)ensureSpace(c,1024*1024);
                    progress.update(240+(int)(250*done/targetFrames),"正在混音 / 淡入淡出");
                }
            }
            original.delete();music.delete();
            encodeAac(mixed,audio,check,(v,m)->progress.update(500+v*4/10,m));
            mixed.delete();
            mux(video,audio,result,check);
            success=true;return result;
        } catch(Exception error) {
            throw new IOException("音轨处理失败："+error.getMessage()+"。可换 MP3/WAV/AAC，或将原声音量设为 0 后重试。",error);
        } finally {for(File f:temporary)f.delete();if(!success)result.delete();}
    }
    private static void decode(Context c,Uri uri,long startUs,long endUs,File output,boolean allowSilent,Check check) throws Exception {
        MediaExtractor extractor=new MediaExtractor();MediaCodec decoder=null;
        try(OutputStream out=new BufferedOutputStream(new FileOutputStream(output),65536)) {
            extractor.setDataSource(c,uri,null);int track=audioTrack(extractor);
            if(track<0){if(allowSilent)return;throw new IOException("文件没有可用音轨");}
            extractor.selectTrack(track);MediaFormat format=extractor.getTrackFormat(track);
            extractor.seekTo(Math.max(0,startUs),MediaExtractor.SEEK_TO_PREVIOUS_SYNC);
            decoder=MediaCodec.createDecoderByType(format.getString(MediaFormat.KEY_MIME));
            format.setInteger(MediaFormat.KEY_PCM_ENCODING,2);
            decoder.configure(format,null,null,0);decoder.start();
            SonicAudioProcessor sonic=null;int previousRate=0,previousChannels=0,previousEncoding=0;
            float[][] weights=null;boolean inputEos=false,outputEos=false;long last=System.nanoTime(),written=0;
            MediaCodec.BufferInfo info=new MediaCodec.BufferInfo();
            byte[] bytes=new byte[65536];
            while(!outputEos) {
                check.check();
                if(System.nanoTime()-last>15_000_000_000L)throw new IOException("音频解码器无响应");
                if(!inputEos) {
                    int index=decoder.dequeueInputBuffer(1000);
                    if(index>=0){ByteBuffer buffer=decoder.getInputBuffer(index);buffer.clear();long pts=extractor.getSampleTime();int size=pts>=endUs?-1:extractor.readSampleData(buffer,0);
                        if(size<0){decoder.queueInputBuffer(index,0,0,0,MediaCodec.BUFFER_FLAG_END_OF_STREAM);inputEos=true;}
                        else{decoder.queueInputBuffer(index,0,size,pts,0);extractor.advance();}last=System.nanoTime();}
                }
                int index=decoder.dequeueOutputBuffer(info,1000);
                if(index<0)continue;last=System.nanoTime();
                try {
                    if(info.size>0) {
                        MediaFormat actual=decoder.getOutputFormat(index);
                        int rate=actual.getInteger(MediaFormat.KEY_SAMPLE_RATE),channels=actual.getInteger(MediaFormat.KEY_CHANNEL_COUNT);
                        int encoding=actual.containsKey(MediaFormat.KEY_PCM_ENCODING)?actual.getInteger(MediaFormat.KEY_PCM_ENCODING):2;
                        if(rate<8000||rate>192000||channels<1||channels>32)throw new IOException("不支持的采样率或声道数");
                        if(sonic==null){sonic=new SonicAudioProcessor();sonic.setOutputSampleRateHz(RATE);sonic.configure(new AudioProcessor.AudioFormat(rate,2,2));sonic.flush(AudioProcessor.StreamMetadata.DEFAULT);previousRate=rate;previousChannels=channels;previousEncoding=encoding;weights=PureJavaMp3Encoder.createDownmixWeights(channels,actual.containsKey(MediaFormat.KEY_CHANNEL_MASK)?actual.getInteger(MediaFormat.KEY_CHANNEL_MASK):0);}
                        if(rate!=previousRate||channels!=previousChannels||encoding!=previousEncoding)throw new IOException("音轨中途改变了采样格式，请先单独转换为 WAV");
                        int frameBytes=PcmMath.sampleBytes(encoding)*channels;
                        int frames=info.size/frameBytes;
                        long skip=Math.max(0,(long)Math.ceil((startUs-info.presentationTimeUs)*rate/1e6));
                        long available=endUs==Long.MAX_VALUE?frames:(long)Math.ceil((endUs-info.presentationTimeUs)*rate/1e6);
                        int first=(int)Math.min(frames,skip),limit=(int)Math.min(frames,Math.max(0,available));
                        if(limit>first) {
                            ByteBuffer buffer=decoder.getOutputBuffer(index).duplicate();buffer.position(info.offset+first*frameBytes);buffer.limit(info.offset+limit*frameBytes);
                            // Preserve an initial audio/video offset as silence.
                            if(written==0){long gap=Math.max(0,Math.round((info.presentationTimeUs+first*1e6/rate-startUs)/1e6*RATE));if(gap*4>MAX_PCM_BYTES)throw new IOException("音轨时间戳异常");writeSilence(out,gap*4,check);written+=gap*4;}
                            ByteBuffer pcm=PcmMath.stereo(buffer.slice(),encoding,channels,weights);
                            if(sonic.isActive()){sonic.queueInput(pcm);written+=drainSonic(sonic,out,bytes,check);}else{written+=writeBuffer(pcm,out,bytes,check);}
                            if(written>MAX_PCM_BYTES)throw new IOException("音频过长，请分段转换");
                            if((written&1048575)<65536)ensureSpace(c,2*1024*1024);
                        }
                    }
                    outputEos=(info.flags&MediaCodec.BUFFER_FLAG_END_OF_STREAM)!=0;
                } finally {decoder.releaseOutputBuffer(index,false);}
            }
            if(sonic!=null&&sonic.isActive()){sonic.queueEndOfStream();drainSonic(sonic,out,bytes,check);sonic.reset();}
        } catch(Exception e){output.delete();throw e;}
        finally{if(decoder!=null){try{decoder.stop();}catch(Exception ignored){}decoder.release();}extractor.release();}
    }
    private static void speed(File input,File output,boolean reverse,double speed,Check check)throws Exception {
        SonicAudioProcessor sonic=new SonicAudioProcessor();sonic.setSpeed((float)speed);sonic.setPitch(1f);sonic.configure(new AudioProcessor.AudioFormat(RATE,2,2));sonic.flush(AudioProcessor.StreamMetadata.DEFAULT);
        try(RandomAccessFile in=new RandomAccessFile(input,"r");OutputStream out=new BufferedOutputStream(new FileOutputStream(output),65536)) {
            byte[] bytes=new byte[32768],scratch=new byte[65536];long length=in.length()/4*4,done=0;
            while(done<length){check.check();int n=(int)Math.min(bytes.length,length-done);in.seek(reverse?length-done-n:done);in.readFully(bytes,0,n);if(reverse)PcmMath.reverseStereo(bytes,n);
                if(sonic.isActive()){ByteBuffer b=ByteBuffer.allocateDirect(n).order(ByteOrder.nativeOrder());b.put(bytes,0,n).flip();sonic.queueInput(b);drainSonic(sonic,out,scratch,check);}else out.write(bytes,0,n);done+=n;}
            if(sonic.isActive()){sonic.queueEndOfStream();drainSonic(sonic,out,scratch,check);}
        }finally{sonic.reset();}
    }
    private static long drainSonic(SonicAudioProcessor sonic,OutputStream out,byte[] bytes,Check check)throws Exception {
        long total=0;ByteBuffer b;while((b=sonic.getOutput()).hasRemaining())total+=writeBuffer(b,out,bytes,check);return total;
    }
    private static long writeBuffer(ByteBuffer b,OutputStream out,byte[] bytes,Check check)throws Exception {long total=0;while(b.hasRemaining()){check.check();int n=Math.min(bytes.length,b.remaining());b.get(bytes,0,n);out.write(bytes,0,n);total+=n;}return total;}
    private static void writeSilence(OutputStream out,long bytes,Check check)throws Exception {byte[] zero=new byte[32768];while(bytes>0){check.check();int n=(int)Math.min(zero.length,bytes);out.write(zero,0,n);bytes-=n;}}
    private static void copyExact(File file,OutputStream out,long bytes,Check check)throws Exception {
        try(InputStream in=new BufferedInputStream(new FileInputStream(file))){byte[] b=new byte[65536];while(bytes>0){check.check();int n=in.read(b,0,(int)Math.min(b.length,bytes));if(n<0)break;out.write(b,0,n);bytes-=n;}writeSilence(out,bytes,check);}
    }
    private static void readLoop(RandomAccessFile file,byte[] b,int n,boolean loop)throws IOException {
        Arrays.fill(b,0,n,(byte)0);int position=0;long length=file.length()/4*4;if(length==0)return;
        while(position<n){int count=(int)Math.min(n-position,length-file.getFilePointer());if(count==0){if(!loop)return;file.seek(0);continue;}file.readFully(b,position,count);position+=count;}
    }
    static void encodeAac(File pcm,File output,Check check,Progress progress)throws Exception {
        MediaCodec codec=null;MediaMuxer muxer=null;boolean started=false;
        try(RandomAccessFile in=new RandomAccessFile(pcm,"r")) {
            codec=MediaCodec.createEncoderByType("audio/mp4a-latm");MediaFormat f=MediaFormat.createAudioFormat("audio/mp4a-latm",RATE,2);
            f.setInteger(MediaFormat.KEY_AAC_PROFILE,MediaCodecInfo.CodecProfileLevel.AACObjectLC);f.setInteger(MediaFormat.KEY_BIT_RATE,192000);f.setInteger(MediaFormat.KEY_MAX_INPUT_SIZE,32768);
            codec.configure(f,null,null,MediaCodec.CONFIGURE_FLAG_ENCODE);codec.start();muxer=new MediaMuxer(output.toString(),MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            int track=-1;boolean inputEnd=false,outputEnd=false;long total=in.length()/4*4,sent=0,last=System.nanoTime();byte[] bytes=new byte[32768];MediaCodec.BufferInfo info=new MediaCodec.BufferInfo();
            while(!outputEnd){check.check();if(System.nanoTime()-last>15_000_000_000L)throw new IOException("AAC 编码器无响应");
                if(!inputEnd){int index=codec.dequeueInputBuffer(1000);if(index>=0){ByteBuffer b=codec.getInputBuffer(index);b.clear();int n=(int)Math.min(Math.min(bytes.length,b.remaining()/4*4),total-sent);if(n>0){in.readFully(bytes,0,n);b.put(bytes,0,n);}codec.queueInputBuffer(index,0,n,(sent/4)*1000000/RATE,n==0?MediaCodec.BUFFER_FLAG_END_OF_STREAM:0);sent+=n;inputEnd=n==0;last=System.nanoTime();}}
                int index=codec.dequeueOutputBuffer(info,1000);
                if(index==MediaCodec.INFO_OUTPUT_FORMAT_CHANGED){if(started)throw new IOException("AAC 格式重复改变");track=muxer.addTrack(codec.getOutputFormat());muxer.start();started=true;last=System.nanoTime();}
                else if(index>=0){last=System.nanoTime();try{if(info.size>0&&(info.flags&MediaCodec.BUFFER_FLAG_CODEC_CONFIG)==0){if(!started)throw new IOException("AAC 封装器尚未就绪");ByteBuffer b=codec.getOutputBuffer(index);b.position(info.offset);b.limit(info.offset+info.size);muxer.writeSampleData(track,b,info);}outputEnd=(info.flags&MediaCodec.BUFFER_FLAG_END_OF_STREAM)!=0;}finally{codec.releaseOutputBuffer(index,false);}}
                progress.update((int)(990*sent/Math.max(1,total)),"正在编码 AAC · 48 kHz · 192 kbps");
            }
            if(!started)throw new IOException("AAC 编码器未输出数据");muxer.stop();started=false;
        }finally{if(codec!=null){try{codec.stop();}catch(Exception ignored){}codec.release();}if(muxer!=null){if(started)try{muxer.stop();}catch(Exception ignored){}muxer.release();}}
    }
    private static void mux(File video,File audio,File output,Check check)throws Exception {
        MediaExtractor v=new MediaExtractor(),a=new MediaExtractor();MediaMuxer muxer=null;boolean started=false;
        try{v.setDataSource(video.toString());a.setDataSource(audio.toString());muxer=new MediaMuxer(output.toString(),MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            int vt=find(v,"video/"),at=find(a,"audio/");if(vt<0||at<0)throw new IOException("合成所需音轨或画面缺失");
            MediaFormat vf=v.getTrackFormat(vt);if(vf.containsKey(MediaFormat.KEY_ROTATION))muxer.setOrientationHint(vf.getInteger(MediaFormat.KEY_ROTATION));
            int vo=muxer.addTrack(vf),ao=muxer.addTrack(a.getTrackFormat(at));v.selectTrack(vt);a.selectTrack(at);muxer.start();started=true;
            ByteBuffer buffer=ByteBuffer.allocateDirect(1024*1024);MediaCodec.BufferInfo info=new MediaCodec.BufferInfo();
            while(v.getSampleTime()>=0||a.getSampleTime()>=0){check.check();boolean useVideo=v.getSampleTime()>=0&&(a.getSampleTime()<0||v.getSampleTime()<=a.getSampleTime());MediaExtractor e=useVideo?v:a;long size=e.getSampleSize();if(size>32*1024*1024)throw new IOException("单个媒体数据包过大");if(size>buffer.capacity())buffer=ByteBuffer.allocateDirect((int)size);buffer.clear();int n=e.readSampleData(buffer,0);if(n<0)break;info.set(0,n,e.getSampleTime(),(e.getSampleFlags()&MediaExtractor.SAMPLE_FLAG_SYNC)!=0?MediaCodec.BUFFER_FLAG_KEY_FRAME:0);muxer.writeSampleData(useVideo?vo:ao,buffer,info);e.advance();}
            muxer.stop();started=false;
        }finally{v.release();a.release();if(muxer!=null){if(started)try{muxer.stop();}catch(Exception ignored){}muxer.release();}}
    }
    static void writeWav(File pcm,File output,Check check)throws Exception {
        long size=pcm.length();if(size>0xffffffffL-36)throw new IOException("WAV 超过 4 GB 上限");
        try(OutputStream out=new BufferedOutputStream(new FileOutputStream(output),65536)) {
            ByteBuffer b=ByteBuffer.allocate(44).order(ByteOrder.LITTLE_ENDIAN);b.put("RIFF".getBytes("US-ASCII")).putInt((int)(size+36)).put("WAVEfmt ".getBytes("US-ASCII")).putInt(16).putShort((short)1).putShort((short)2).putInt(RATE).putInt(RATE*4).putShort((short)4).putShort((short)16).put("data".getBytes("US-ASCII")).putInt((int)size);out.write(b.array());copyExact(pcm,out,size,check);
        }
    }
    private static long videoDuration(File video)throws IOException {MediaExtractor e=new MediaExtractor();try{e.setDataSource(video.toString());int t=find(e,"video/");if(t<0)throw new IOException("没有视频画面");return e.getTrackFormat(t).getLong(MediaFormat.KEY_DURATION);}finally{e.release();}}
    private static int audioTrack(MediaExtractor e){return find(e,"audio/");}
    private static int find(MediaExtractor e,String prefix){for(int i=0;i<e.getTrackCount();i++){String mime=e.getTrackFormat(i).getString(MediaFormat.KEY_MIME);if(mime!=null&&mime.startsWith(prefix))return i;}return -1;}
    private static File temp(Context c,String ext)throws IOException{return File.createTempFile("audio_",ext,c.getCacheDir());}
    private static void ensureSpace(Context c,long bytes)throws IOException{if(c.getCacheDir().getUsableSpace()<bytes+32L*1024*1024)throw new IOException("音频临时存储不足，请缩短片段或清理空间");}
}
''',
    'app/src/main/java/com/qi/formatconverter/DocumentKit.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.net.Uri;
import android.util.Xml;
import com.tom_roush.pdfbox.android.PDFBoxResourceLoader;
import com.tom_roush.pdfbox.io.MemoryUsageSetting;
import com.tom_roush.pdfbox.pdmodel.PDDocument;
import com.tom_roush.pdfbox.text.PDFTextStripper;
import com.tom_roush.pdfbox.multipdf.PDFMergerUtility;
import org.xmlpull.v1.XmlPullParser;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.zip.*;

/** Offline document interchange. Office/EPUB conversion preserves readable text, not layout. */
final class DocumentKit {
    static final int MAX_TEXT = 16 * 1024 * 1024;
    private static final long MAX_ARCHIVE = 128L * 1024 * 1024;
    interface Check { void check() throws Exception; }
    private DocumentKit() { }

    static String read(Context context, Uri uri, String kind, Check check) throws Exception {
        if ("PDF".equals(kind)) return pdfText(context, uri, check);
        File local = File.createTempFile("document_", ".zip", context.getCacheDir());
        try {
            copy(context, uri, local, MAX_ARCHIVE, check);
            try (ZipFile zip = new ZipFile(local)) {
                if (zip.size() > 10000) throw new IOException("文档包含过多压缩条目");
                if ("DOCX".equals(kind)) return xmlText(entry(zip, "word/document.xml", check), true);
                if ("ODT".equals(kind)) return xmlText(entry(zip, "content.xml", check), false);
                String container = entry(zip, "META-INF/container.xml", check);
                XmlPullParser parser = parser(container);
                String root = null;
                for (int event = parser.getEventType(); event != XmlPullParser.END_DOCUMENT; event = parser.next()) {
                    if (event == XmlPullParser.START_TAG && "rootfile".equals(parser.getName())) {
                        root = parser.getAttributeValue(null, "full-path"); break;
                    }
                }
                if (root == null) throw new IOException("EPUB 缺少阅读顺序定义");
                String base = root.contains("/") ? root.substring(0, root.lastIndexOf('/') + 1) : "";
                parser = parser(entry(zip, root, check));
                Map<String,String> paths = new HashMap<>();
                List<String> spine = new ArrayList<>();
                for (int event = parser.getEventType(); event != XmlPullParser.END_DOCUMENT; event = parser.next()) {
                    if (event != XmlPullParser.START_TAG) continue;
                    if ("item".equals(parser.getName())) paths.put(parser.getAttributeValue(null,"id"), parser.getAttributeValue(null,"href"));
                    if ("itemref".equals(parser.getName())) spine.add(parser.getAttributeValue(null,"idref"));
                }
                if (spine.isEmpty()) throw new IOException("EPUB 没有正文阅读顺序");
                StringBuilder text = new StringBuilder();
                for (String id : spine) {
                    check.check();
                    String href = paths.get(id);
                    if (href == null) throw new IOException("EPUB 章节缺失：" + id);
                    String path = new java.net.URI(base).resolve(href).normalize().getPath();
                    append(text, TextConverter.htmlToText(entry(zip, path, check)) + "\n\n");
                }
                return text.toString();
            }
        } finally { local.delete(); }
    }

    private static XmlPullParser parser(String xml) throws Exception {
        if (xml.toUpperCase(Locale.ROOT).contains("<!DOCTYPE") || xml.contains("<!ENTITY"))
            throw new IOException("不支持含外部实体或 DTD 的文档");
        XmlPullParser parser = Xml.newPullParser();
        parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, true);
        parser.setInput(new StringReader(xml));
        return parser;
    }

    private static String xmlText(String xml, boolean docx) throws Exception {
        XmlPullParser parser = parser(xml);
        StringBuilder text = new StringBuilder();
        boolean inText = false;
        for (int event = parser.getEventType(); event != XmlPullParser.END_DOCUMENT; event = parser.next()) {
            String name = parser.getName();
            if (event == XmlPullParser.START_TAG) {
                if ("t".equals(name)) inText = true;
                if ("tab".equals(name)) append(text, "\t");
                if ("br".equals(name) || "line-break".equals(name)) append(text,"\n");
                if (!docx && "s".equals(name)) {
                    int count = 1;
                    String value = parser.getAttributeValue("urn:oasis:names:tc:opendocument:xmlns:text:1.0", "c");
                    if (value != null) count = Math.min(1000, Math.max(1, Integer.parseInt(value)));
                    for (int i=0;i<count;i++) append(text," ");
                }
            } else if (event == XmlPullParser.TEXT && (!docx || inText)) {
                append(text, parser.getText());
            } else if (event == XmlPullParser.END_TAG) {
                if ("t".equals(name)) inText = false;
                if ("p".equals(name) || "h".equals(name) || "tr".equals(name)) append(text,"\n");
                if ("tc".equals(name) || "table-cell".equals(name)) append(text,"\t");
            }
        }
        return text.toString().trim();
    }

    private static String entry(ZipFile zip, String name, Check check) throws Exception {
        ZipEntry entry = zip.getEntry(name);
        if (entry == null || entry.isDirectory()) throw new IOException("文档条目缺失：" + name);
        if (entry.getSize() > MAX_TEXT) throw new IOException("解压后的文档过大");
        try (InputStream in = zip.getInputStream(entry); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] bytes = new byte[16384]; int n;
            while ((n = in.read(bytes)) != -1) {
                check.check();
                if ((long)out.size()+n > MAX_TEXT) throw new IOException("解压后的文档超过 16 MB");
                out.write(bytes,0,n);
            }
            return TextConverter.decode(out.toByteArray());
        }
    }

    static void copy(Context context, Uri uri, File output, long limit, Check check) throws Exception {
        try (InputStream in = context.getContentResolver().openInputStream(uri);
             OutputStream out = new BufferedOutputStream(new FileOutputStream(output))) {
            if (in == null) throw new IOException("无法打开文档");
            byte[] bytes = new byte[65536]; long count=0; int n;
            while ((n=in.read(bytes))!=-1) {
                check.check(); count+=n;
                if (count>limit) throw new IOException("文档超过支持的大小上限");
                if (output.getParentFile().getUsableSpace()<32L*1024*1024) throw new IOException("临时存储空间不足");
                out.write(bytes,0,n);
            }
        }
    }

    private static MemoryUsageSetting memory(Context context) {
        return MemoryUsageSetting.setupMixed(8L*1024*1024,256L*1024*1024).setTempDir(context.getCacheDir());
    }

    private static String pdfText(Context context, Uri uri, Check check) throws Exception {
        PDFBoxResourceLoader.init(context.getApplicationContext());
        File local=File.createTempFile("document_", ".pdf",context.getCacheDir());
        try {
            copy(context,uri,local,MAX_ARCHIVE,check);
            try (PDDocument document=PDDocument.load(local, memory(context))) {
                if (!document.getCurrentAccessPermission().canExtractContent()) throw new IOException("此 PDF 不允许提取文本");
                if (document.getNumberOfPages()>2000) throw new IOException("PDF 超过 2000 页，请先拆分");
                StringBuilder text=new StringBuilder();
                Writer writer=new Writer() {
                    public void write(char[] chars,int off,int len) throws IOException {
                        if (Thread.currentThread().isInterrupted()) throw new InterruptedIOException("已取消");
                        if ((long)text.length()+len>MAX_TEXT) throw new IOException("提取的文本超过 16 MB");
                        text.append(chars,off,len);
                    }
                    public void flush() { }
                    public void close() { }
                };
                PDFTextStripper stripper=new PDFTextStripper();
                stripper.setSortByPosition(true);
                for (int p=1;p<=document.getNumberOfPages();p++) {
                    check.check(); stripper.setStartPage(p); stripper.setEndPage(p); stripper.writeText(document,writer);
                }
                if (text.toString().trim().isEmpty()) throw new IOException("此 PDF 没有可提取文字，可能是扫描件；请先 OCR 识别。此功能不包含 OCR。");
                return java.text.Normalizer.normalize(text.toString(), java.text.Normalizer.Form.NFKC);
            }
        } finally { local.delete(); }
    }

    static void mergePdf(Context context,List<Uri> uris,File output,Check check) throws Exception {
        PDFBoxResourceLoader.init(context.getApplicationContext());
        try (PDDocument result=new PDDocument(memory(context))) {
            PDFMergerUtility merger=new PDFMergerUtility();
            for (Uri uri:uris) {
                check.check();
                File local=File.createTempFile("document_", ".pdf",context.getCacheDir());
                try {
                    copy(context,uri,local,MAX_ARCHIVE,check);
                    try (PDDocument source=PDDocument.load(local,memory(context))) {
                        if (source.getNumberOfPages()+result.getNumberOfPages()>2000) throw new IOException("合并后超过 2000 页");
                        merger.appendDocument(result,source);
                    }
                } finally { local.delete(); }
            }
            check.check(); result.save(output);
        }
    }

    static void write(File output,int format,String text,String title,Check check) throws Exception {
        if (format==28) {
            try (Writer out=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output),StandardCharsets.US_ASCII))) {
                out.write("{\\rtf1\\ansi\\deff0\\uc1 ");
                for (int i=0;i<text.length();i++) {
                    if ((i&4095)==0) check.check();
                    char c=text.charAt(i);
                    if (c=='\n') out.write("\\par\n");
                    else if (c=='\r') { }
                    else if (c=='\t') out.write("\\tab ");
                    else if (c=='\\'||c=='{'||c=='}') out.write("\\"+c);
                    else if (c>=32&&c<127) out.write(c);
                    else out.write("\\u"+(short)c+"?");
                }
                out.write('}');
            }
            return;
        }
        try (ZipOutputStream zip=new ZipOutputStream(new BufferedOutputStream(new FileOutputStream(output)))) {
            zip.setLevel(Deflater.BEST_SPEED);
            if (format==24) {
                put(zip,"[Content_Types].xml","<?xml version=\"1.0\"?><Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"><Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/></Types>");
                put(zip,"_rels/.rels","<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"r1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/></Relationships>");
                zip.putNextEntry(new ZipEntry("word/document.xml"));
                raw(zip,"<?xml version=\"1.0\" encoding=\"UTF-8\"?><w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:body>");
                for (String line:text.split("\\R",-1)) { check.check(); raw(zip,"<w:p><w:r><w:t xml:space=\"preserve\">"+escape(line)+"</w:t></w:r></w:p>"); }
                raw(zip,"<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/></w:sectPr></w:body></w:document>"); zip.closeEntry();
            } else if (format==25) {
                stored(zip,"mimetype","application/epub+zip");
                put(zip,"META-INF/container.xml","<?xml version=\"1.0\"?><container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\"><rootfiles><rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/></rootfiles></container>");
                String id="urn:uuid:"+UUID.randomUUID();
                put(zip,"OEBPS/content.opf","<package xmlns=\"http://www.idpf.org/2007/opf\" version=\"3.0\" unique-identifier=\"book-id\"><metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"><dc:identifier id=\"book-id\">"+id+"</dc:identifier><dc:title>"+escape(title)+"</dc:title><dc:language>zh</dc:language><meta property=\"dcterms:modified\">"+java.time.Instant.now().truncatedTo(java.time.temporal.ChronoUnit.SECONDS)+"</meta></metadata><manifest><item id=\"body\" href=\"body.xhtml\" media-type=\"application/xhtml+xml\"/><item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/></manifest><spine><itemref idref=\"body\"/></spine></package>");
                put(zip,"OEBPS/nav.xhtml","<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\"><head><title>目录</title></head><body><nav epub:type=\"toc\"><ol><li><a href=\"body.xhtml\">正文</a></li></ol></nav></body></html>");
                zip.putNextEntry(new ZipEntry("OEBPS/body.xhtml")); raw(zip,"<html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>"+escape(title)+"</title></head><body>");
                for(String line:text.split("\\R",-1)){check.check();raw(zip,"<p>"+escape(line)+"</p>");}
                raw(zip,"</body></html>");zip.closeEntry();
            } else if (format==26) {
                stored(zip,"mimetype","application/vnd.oasis.opendocument.text");
                put(zip,"META-INF/manifest.xml","<manifest:manifest xmlns:manifest=\"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0\" manifest:version=\"1.2\"><manifest:file-entry manifest:full-path=\"/\" manifest:media-type=\"application/vnd.oasis.opendocument.text\"/><manifest:file-entry manifest:full-path=\"content.xml\" manifest:media-type=\"text/xml\"/></manifest:manifest>");
                zip.putNextEntry(new ZipEntry("content.xml"));raw(zip,"<office:document-content xmlns:office=\"urn:oasis:names:tc:opendocument:xmlns:office:1.0\" xmlns:text=\"urn:oasis:names:tc:opendocument:xmlns:text:1.0\" office:version=\"1.2\"><office:body><office:text>");
                for(String line:text.split("\\R",-1)){check.check();raw(zip,"<text:p>"+escape(line).replace(" ","<text:s/>").replace("\t","<text:tab/>")+"</text:p>");}
                raw(zip,"</office:text></office:body></office:document-content>");zip.closeEntry();
            } else throw new IOException("不支持的文档输出格式");
        }
    }
    static String escape(String text) {
        return text.replaceAll("[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F]", "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\"","&quot;");
    }
    static String html(String text,String title) { return "<!doctype html><html lang=\"zh\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width\"><title>"+escape(title)+"</title><style>body{max-width:50rem;margin:2rem auto;padding:1rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;line-height:1.6}</style><pre>"+escape(text)+"</pre></html>"; }
    private static void append(StringBuilder b,String s) throws IOException { if((long)b.length()+s.length()>MAX_TEXT)throw new IOException("正文超过 16 MB");b.append(s); }
    private static void raw(ZipOutputStream z,String s)throws IOException{z.write(s.getBytes(StandardCharsets.UTF_8));}
    private static void put(ZipOutputStream z,String n,String s)throws IOException{z.putNextEntry(new ZipEntry(n));raw(z,s);z.closeEntry();}
    private static void stored(ZipOutputStream z,String n,String s)throws IOException{byte[] b=s.getBytes(StandardCharsets.UTF_8);CRC32 crc=new CRC32();crc.update(b);ZipEntry e=new ZipEntry(n);e.setMethod(ZipEntry.STORED);e.setSize(b.length);e.setCompressedSize(b.length);e.setCrc(crc.getValue());z.putNextEntry(e);z.write(b);z.closeEntry();}
}
''',
    'app/src/main/java/com/qi/formatconverter/EditorPreviewRenderer.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.media.MediaMetadataRetriever;
import android.net.Uri;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Latest-frame-only software renderer used to preview color/crop edits over a playing VideoView. */
final class EditorPreviewRenderer {
    interface Listener {
        void onFrame(Bitmap bitmap);
    }

    private static final class Request {
        final long id;
        final Uri uri;
        final long positionMs;
        final AnimationEdits edits;
        final int maxWidth;
        final int maxHeight;
        final Listener listener;

        Request(long id, Uri uri, long positionMs, AnimationEdits edits,
                int maxWidth, int maxHeight, Listener listener) {
            this.id = id;
            this.uri = uri;
            this.positionMs = positionMs;
            this.edits = edits;
            this.maxWidth = maxWidth;
            this.maxHeight = maxHeight;
            this.listener = listener;
        }
    }

    private final Context context;
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private final Object lock = new Object();
    private MediaMetadataRetriever retriever;
    private String retrieverUri;
    private int sourceWidth=1, sourceHeight=1;
    private Request latest;
    private boolean draining;
    private boolean closed;
    private long nextId;

    EditorPreviewRenderer(Context context) {
        this.context = context.getApplicationContext();
    }

    void request(Uri uri, long positionMs, AnimationEdits edits,
                 int maxWidth, int maxHeight, Listener listener) {
        if (uri == null || edits == null || listener == null) return;
        synchronized (lock) {
            if (closed) return;
            long id = ++nextId;
            latest = new Request(id, uri, Math.max(0L, positionMs), edits,
                    Math.max(64, maxWidth), Math.max(64, maxHeight), listener);
            if (!draining) {
                draining = true;
                worker.execute(this::drain);
            }
        }
    }

    private void drain() {
        while (true) {
            Request request;
            synchronized (lock) {
                if (closed) {
                    draining = false;
                    break;
                }
                request = latest;
                latest = null;
                if (request == null) {
                    draining = false;
                    break;
                }
            }

            Bitmap frame = null;
            try {
                frame = render(request);
            } catch (Throwable ignored) { }

            boolean deliver;
            synchronized (lock) {
                // Always publish a completed frame. If decoding one frame takes longer than the
                // request interval, requiring request.id == newestId starves delivery forever:
                // every completed frame is considered stale because a newer request arrived while
                // it was decoding. The single-slot `latest` queue still skips intermediate work,
                // and the owner rejects frames from an obsolete source generation.
                deliver = !closed;
            }
            if (frame != null) {
                if (deliver) request.listener.onFrame(frame);
                else if (!frame.isRecycled()) frame.recycle();
            }
        }
    }

    private Bitmap render(Request request) throws Exception {
        ensureRetriever(request.uri);
        long timeUs = Math.max(0L, request.positionMs) * 1000L;
        double previewScale=Math.min(1.0,960.0/Math.max(request.maxWidth,request.maxHeight));
        int targetWidth=Math.max(64,(int)(request.maxWidth*previewScale));
        int targetHeight=Math.max(64,(int)(request.maxHeight*previewScale));
        int[] bounds=FrameEditor.decodeBounds(sourceWidth,sourceHeight,targetWidth,targetHeight,request.edits);
        Bitmap raw = retriever.getScaledFrameAtTime(timeUs, MediaMetadataRetriever.OPTION_CLOSEST,
                Math.max(64,bounds[0]),Math.max(64,bounds[1]));
        if (raw == null) raw = retriever.getScaledFrameAtTime(timeUs,
                MediaMetadataRetriever.OPTION_CLOSEST_SYNC,Math.max(64,bounds[0]),Math.max(64,bounds[1]));
        if (raw == null) return null;

        try {
            int[] edited = FrameEditor.editedSize(raw.getWidth(), raw.getHeight(), request.edits);
            double scale = Math.min(
                    targetWidth / (double) Math.max(1, edited[0]),
                    targetHeight / (double) Math.max(1, edited[1]));
            scale = Math.min(1.0, Math.max(0.05, scale));
            int width = Math.max(1, (int) Math.round(edited[0] * scale));
            int height = Math.max(1, (int) Math.round(edited[1] * scale));
            Bitmap output = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(output);
            FrameEditor.drawBitmap(canvas, raw, 0xFF000000,
                    request.edits, FrameEditor.createPaint(request.edits));
            return output;
        } finally {
            if (!raw.isRecycled()) raw.recycle();
        }
    }

    private void ensureRetriever(Uri uri) throws Exception {
        String value = uri.toString();
        if (retriever != null && value.equals(retrieverUri)) return;
        releaseRetriever();
        retriever = new MediaMetadataRetriever();
        retriever.setDataSource(context, uri);
        sourceWidth=metadataInt(MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH,1280);
        sourceHeight=metadataInt(MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT,720);
        int rotation=metadataInt(MediaMetadataRetriever.METADATA_KEY_VIDEO_ROTATION,0);
        if(rotation==90||rotation==270){int swap=sourceWidth;sourceWidth=sourceHeight;sourceHeight=swap;}
        retrieverUri = value;
    }

    void close() {
        synchronized (lock) {
            if (closed) return;
            closed = true;
            latest = null;
        }
        // Release on the owning thread after the current native decode finishes.
        // Releasing concurrently with getScaledFrameAtTime can crash vendor codecs.
        worker.execute(this::releaseRetriever);
        worker.shutdown();
    }

    private int metadataInt(int key,int fallback) {
        try{return Integer.parseInt(retriever.extractMetadata(key));}catch(Exception ignored){return fallback;}
    }

    private synchronized void releaseRetriever() {
        if (retriever != null) {
            try { retriever.release(); } catch (Exception ignored) { }
            retriever = null;
            retrieverUri = null;
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/EditorTimelineView.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.MotionEvent;
import android.view.View;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Compact clip-style timeline. Each kept piece is a block separated by a visible edit gap. */
final class EditorTimelineView extends View {
    interface OnSeekListener {
        void onSeek(double seconds, boolean finished);
    }

    private static final double EPS = 0.0005;
    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final RectF bar = new RectF();
    private double durationSeconds = 1.0;
    private double positionSeconds;
    private double splitPoint1 = Double.NaN;
    private double splitPoint2 = Double.NaN;
    private List<AnimationEdits.TimeRange> deletedRanges = Collections.emptyList();
    private List<AnimationEdits.TimeRange> reversedRanges = Collections.emptyList();
    private List<Double> sourceBoundaries = Collections.emptyList();
    private OnSeekListener seekListener;
    private boolean dragging;

    EditorTimelineView(Context context) {
        super(context);
        setClickable(true);
        setFocusable(true);
    }

    void setDurationSeconds(double value) {
        durationSeconds = Math.max(0.001, value);
        positionSeconds = nearestKeptSource(positionSeconds);
        invalidate();
    }

    void setPositionSeconds(double value) {
        positionSeconds = nearestKeptSource(value);
        invalidate();
    }

    double getPositionSeconds() {
        return positionSeconds;
    }

    void setSplitPoints(double first, double second) {
        splitPoint1 = first;
        splitPoint2 = second;
        invalidate();
    }

    void setSourceBoundaries(List<Double> values) {
        if (values == null || values.isEmpty()) {
            sourceBoundaries = Collections.emptyList();
            invalidate();
            return;
        }
        List<Double> clean = new ArrayList<>();
        for (Double value : values) {
            if (value == null || Double.isNaN(value) || Double.isInfinite(value)) continue;
            double point = Math.max(0.0, Math.min(durationSeconds, value));
            if (point <= EPS || point >= durationSeconds - EPS) continue;
            clean.add(point);
        }
        Collections.sort(clean);
        List<Double> unique = new ArrayList<>();
        for (double point : clean) {
            if (unique.isEmpty() || Math.abs(point - unique.get(unique.size() - 1)) >= 0.01) {
                unique.add(point);
            }
        }
        sourceBoundaries = Collections.unmodifiableList(unique);
        invalidate();
    }

    void setRanges(List<AnimationEdits.TimeRange> deleted,
                   List<AnimationEdits.TimeRange> reversed) {
        AnimationEdits normalized = new AnimationEdits(
                0, 0, 1.0, AnimationEdits.CROP_NONE, 0, false, false,
                0, 100, 100,
                deleted == null ? Collections.emptyList() : deleted,
                reversed == null ? Collections.emptyList() : reversed);
        deletedRanges = normalized.deletedRanges;
        reversedRanges = normalized.reversedRanges;
        positionSeconds = nearestKeptSource(positionSeconds);
        invalidate();
    }

    /** All persistent clip edges: source-file borders plus both sides of every removed range. */
    List<Double> getEditingBoundaries() {
        List<Double> points = new ArrayList<>();
        points.add(0.0);
        points.add(durationSeconds);
        points.addAll(sourceBoundaries);
        for (AnimationEdits.TimeRange range : deletedRanges) {
            double start = Math.max(0.0, Math.min(durationSeconds, range.startSeconds));
            double end = Math.max(start, Math.min(durationSeconds, range.endSeconds));
            points.add(start);
            points.add(end);
        }
        Collections.sort(points);
        List<Double> unique = new ArrayList<>();
        for (double point : points) {
            if (unique.isEmpty() || Math.abs(point - unique.get(unique.size() - 1)) >= 0.01) {
                unique.add(point);
            }
        }
        return unique;
    }

    double getVisibleDurationSeconds() {
        return visibleDurationSeconds();
    }

    double getVisibleOffsetSeconds(double sourceSeconds) {
        return visibleOffsetForSource(sourceSeconds);
    }

    void setOnSeekListener(OnSeekListener listener) {
        seekListener = listener;
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int height = Math.round(dp(42));
        int resolvedWidth = resolveSize(Math.round(dp(240)), widthMeasureSpec);
        setMeasuredDimension(resolvedWidth, resolveSize(height, heightMeasureSpec));
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float left = dp(8);
        float right = getWidth() - dp(8);
        float centerY = getHeight() * 0.60f;
        float thickness = dp(9);
        bar.set(left, centerY - thickness * 0.5f, right, centerY + thickness * 0.5f);

        List<SegmentLayout> layouts = buildLayouts(left, right);
        paint.setStyle(Paint.Style.FILL);
        if (layouts.isEmpty()) {
            paint.setColor(0x44D4D6DE);
            canvas.drawRoundRect(bar, thickness, thickness, paint);
        } else {
            paint.setColor(0xB8D4D6DE);
            for (SegmentLayout layout : layouts) {
                RectF segment = new RectF(layout.left, bar.top, layout.right, bar.bottom);
                canvas.drawRoundRect(segment, dp(3), dp(3), paint);
            }
            for (AnimationEdits.TimeRange range : reversedRanges) {
                drawRange(canvas, layouts, range, 0xFF7C6CE7);
            }
        }

        drawSplitMarker(canvas, splitPoint1, "1", 0xFFFFC857);
        drawSplitMarker(canvas, splitPoint2, "2", 0xFFFFC857);

        float x = xFor(positionSeconds);
        paint.setColor(0xFFFFFFFF);
        paint.setStrokeWidth(dp(2));
        canvas.drawLine(x, dp(7), x, getHeight() - dp(5), paint);
        paint.setStyle(Paint.Style.FILL);
        android.graphics.Path triangle = new android.graphics.Path();
        triangle.moveTo(x - dp(5), dp(4));
        triangle.lineTo(x + dp(5), dp(4));
        triangle.lineTo(x, dp(10));
        triangle.close();
        canvas.drawPath(triangle, paint);
    }

    private void drawRange(Canvas canvas, List<SegmentLayout> layouts,
                           AnimationEdits.TimeRange range, int color) {
        paint.setColor(color);
        for (SegmentLayout layout : layouts) {
            double start = Math.max(layout.range.startSeconds, range.startSeconds);
            double end = Math.min(layout.range.endSeconds, range.endSeconds);
            if (end - start <= EPS) continue;
            float x1 = xInside(layout, start);
            float x2 = xInside(layout, end);
            if (x2 <= x1) continue;
            RectF segment = new RectF(x1, bar.top, x2, bar.bottom);
            canvas.drawRoundRect(segment, dp(3), dp(3), paint);
        }
    }

    private void drawSplitMarker(Canvas canvas, double seconds, String label, int color) {
        if (Double.isNaN(seconds)) return;
        float x = xFor(seconds);
        paint.setColor(color);
        paint.setStrokeWidth(dp(2));
        canvas.drawLine(x, dp(12), x, getHeight() - dp(5), paint);
        paint.setTextSize(dp(10));
        paint.setTextAlign(Paint.Align.CENTER);
        canvas.drawText(label, x, dp(10), paint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int action = event.getActionMasked();
        if (action == MotionEvent.ACTION_DOWN) {
            dragging = true;
            if (getParent() != null) getParent().requestDisallowInterceptTouchEvent(true);
            updateTouchPosition(event.getX(), false);
            return true;
        }
        if (action == MotionEvent.ACTION_MOVE && dragging) {
            if (getParent() != null) getParent().requestDisallowInterceptTouchEvent(true);
            updateTouchPosition(event.getX(), false);
            return true;
        }
        if ((action == MotionEvent.ACTION_UP || action == MotionEvent.ACTION_CANCEL) && dragging) {
            if (action == MotionEvent.ACTION_UP) updateTouchPosition(event.getX(), true);
            else if (seekListener != null) seekListener.onSeek(positionSeconds, true);
            dragging = false;
            if (getParent() != null) getParent().requestDisallowInterceptTouchEvent(false);
            if (action == MotionEvent.ACTION_UP) performClick();
            return true;
        }
        return super.onTouchEvent(event);
    }

    private void updateTouchPosition(float touchX, boolean finished) {
        positionSeconds = sourceForX(touchX);
        invalidate();
        if (seekListener != null) seekListener.onSeek(positionSeconds, finished);
    }

    @Override
    public boolean performClick() {
        super.performClick();
        return true;
    }

    private float xFor(double seconds) {
        float left = dp(8);
        float right = Math.max(left + 1f, getWidth() - dp(8));
        List<SegmentLayout> layouts = buildLayouts(left, right);
        if (layouts.isEmpty()) return left;
        double source = clamp(seconds);
        for (int i = 0; i < layouts.size(); i++) {
            SegmentLayout current = layouts.get(i);
            if (source < current.range.startSeconds - EPS) {
                if (i == 0) return current.left;
                SegmentLayout previous = layouts.get(i - 1);
                double gapStart = previous.range.endSeconds;
                double gapEnd = current.range.startSeconds;
                if (gapEnd - gapStart <= EPS) return (previous.right + current.left) * 0.5f;
                double ratio = (source - gapStart) / Math.max(EPS, gapEnd - gapStart);
                ratio = Math.max(0.0, Math.min(1.0, ratio));
                return previous.right + (float) ratio * (current.left - previous.right);
            }
            if (source <= current.range.endSeconds + EPS) {
                if (i + 1 < layouts.size()
                        && Math.abs(source - current.range.endSeconds) <= EPS
                        && Math.abs(layouts.get(i + 1).range.startSeconds - source) <= EPS) {
                    return (current.right + layouts.get(i + 1).left) * 0.5f;
                }
                return xInside(current, source);
            }
        }
        return layouts.get(layouts.size() - 1).right;
    }

    private double sourceForX(float touchX) {
        float left = dp(8);
        float right = Math.max(left + 1f, getWidth() - dp(8));
        List<SegmentLayout> layouts = buildLayouts(left, right);
        if (layouts.isEmpty()) return 0.0;
        if (touchX <= layouts.get(0).left) return layouts.get(0).range.startSeconds;
        for (int i = 0; i < layouts.size(); i++) {
            SegmentLayout current = layouts.get(i);
            if (touchX >= current.left && touchX <= current.right) {
                float width = Math.max(1f, current.right - current.left);
                double ratio = (touchX - current.left) / width;
                return clamp(current.range.startSeconds
                        + ratio * (current.range.endSeconds - current.range.startSeconds));
            }
            if (i + 1 < layouts.size()) {
                SegmentLayout next = layouts.get(i + 1);
                if (touchX > current.right && touchX < next.left) {
                    if (Math.abs(current.range.endSeconds - next.range.startSeconds) <= EPS) {
                        return clamp(current.range.endSeconds);
                    }
                    float midpoint = (current.right + next.left) * 0.5f;
                    if (touchX < midpoint) {
                        return clamp(Math.max(current.range.startSeconds,
                                current.range.endSeconds - 0.001));
                    }
                    return clamp(next.range.startSeconds);
                }
            }
        }
        return layouts.get(layouts.size() - 1).range.endSeconds;
    }

    private List<SegmentLayout> buildLayouts(float left, float right) {
        List<AnimationEdits.TimeRange> segments = buildVisibleSegments();
        if (segments.isEmpty()) return Collections.emptyList();
        float width = Math.max(1f, right - left);
        float gap = gapWidthPx(segments.size(), width);
        float contentWidth = Math.max(1f, width - gap * Math.max(0, segments.size() - 1));
        double totalSeconds = 0.0;
        for (AnimationEdits.TimeRange segment : segments) totalSeconds += segment.durationSeconds();
        totalSeconds = Math.max(EPS, totalSeconds);

        List<SegmentLayout> result = new ArrayList<>();
        float x = left;
        for (int i = 0; i < segments.size(); i++) {
            AnimationEdits.TimeRange segment = segments.get(i);
            float segmentWidth = contentWidth * (float) (segment.durationSeconds() / totalSeconds);
            float end = i == segments.size() - 1 ? right : Math.min(right, x + segmentWidth);
            result.add(new SegmentLayout(segment, x, Math.max(x + 1f, end)));
            x = end + gap;
        }
        return result;
    }

    private float gapWidthPx(int segmentCount, float width) {
        if (segmentCount <= 1) return 0f;
        float maxPerGap = width * 0.28f / (segmentCount - 1);
        return Math.max(1f, Math.min(dp(6), maxPerGap));
    }

    private List<AnimationEdits.TimeRange> buildVisibleSegments() {
        List<AnimationEdits.TimeRange> result = new ArrayList<>();
        double cursor = 0.0;
        for (AnimationEdits.TimeRange deleted : deletedRanges) {
            double start = Math.max(cursor, Math.min(durationSeconds, deleted.startSeconds));
            double end = Math.max(start, Math.min(durationSeconds, deleted.endSeconds));
            appendSplitRange(result, cursor, start);
            cursor = Math.max(cursor, end);
            if (cursor >= durationSeconds - EPS) break;
        }
        appendSplitRange(result, cursor, durationSeconds);
        return result;
    }

    private void appendSplitRange(List<AnimationEdits.TimeRange> output,
                                  double start, double end) {
        if (end - start <= EPS) return;
        double cursor = start;
        for (double boundary : sourceBoundaries) {
            if (boundary <= cursor + EPS) continue;
            if (boundary >= end - EPS) break;
            output.add(new AnimationEdits.TimeRange(cursor, boundary));
            cursor = boundary;
        }
        if (end - cursor > EPS) output.add(new AnimationEdits.TimeRange(cursor, end));
    }

    private float xInside(SegmentLayout layout, double seconds) {
        double span = Math.max(EPS, layout.range.durationSeconds());
        double ratio = (seconds - layout.range.startSeconds) / span;
        ratio = Math.max(0.0, Math.min(1.0, ratio));
        return layout.left + (float) ratio * (layout.right - layout.left);
    }

    private double visibleDurationSeconds() {
        double total = 0.0;
        for (AnimationEdits.TimeRange range : buildVisibleSegments()) total += range.durationSeconds();
        return Math.max(0.001, total);
    }

    private double visibleOffsetForSource(double sourceSeconds) {
        double source = clamp(sourceSeconds);
        double removed = 0.0;
        for (AnimationEdits.TimeRange range : deletedRanges) {
            double start = Math.max(0.0, Math.min(durationSeconds, range.startSeconds));
            double end = Math.max(start, Math.min(durationSeconds, range.endSeconds));
            if (source >= end) removed += end - start;
            else if (source > start) {
                removed += source - start;
                break;
            } else break;
        }
        return Math.max(0.0, Math.min(visibleDurationSeconds(), source - removed));
    }

    private double nearestKeptSource(double sourceSeconds) {
        double source = clamp(sourceSeconds);
        for (AnimationEdits.TimeRange range : deletedRanges) {
            if (source >= range.startSeconds && source < range.endSeconds) {
                if (range.endSeconds < durationSeconds) return clamp(range.endSeconds);
                return clamp(Math.max(0.0, range.startSeconds - 0.001));
            }
        }
        return source;
    }

    private double clamp(double value) {
        return Math.max(0.0, Math.min(durationSeconds, value));
    }

    private float dp(float value) {
        return value * getResources().getDisplayMetrics().density;
    }

    private static final class SegmentLayout {
        final AnimationEdits.TimeRange range;
        final float left;
        final float right;

        SegmentLayout(AnimationEdits.TimeRange range, float left, float right) {
            this.range = range;
            this.left = left;
            this.right = right;
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/EditorVideoPlayer.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.media3.common.AudioAttributes;
import androidx.media3.common.C;
import androidx.media3.common.MediaItem;
import androidx.media3.common.PlaybackException;
import androidx.media3.common.Player;
import androidx.media3.common.Tracks;
import androidx.media3.exoplayer.DefaultLoadControl;
import androidx.media3.exoplayer.DefaultRenderersFactory;
import androidx.media3.exoplayer.ExoPlayer;
import java.util.function.Consumer;

/** Software image preview with a separate audio-only Media3 player.
 * No video Surface is allocated. Unsupported audio falls back to the image clock;
 * preview failures never change export settings or prevent timeline editing.
 */
final class EditorVideoPlayer extends FrameLayout {
    interface OnPreparedListener {
        void onPrepared(EditorVideoPlayer player);
    }

    interface OnCompletionListener {
        void onCompletion(EditorVideoPlayer player);
    }

    private static final long FRAME_TICK_MS = 140L;

    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private final ImageView frameView;
    private final TextView statusView;
    private final EditorPreviewRenderer renderer;

    private Uri uri;
    private boolean logicalPlaying;
    private boolean detached;
    private boolean preparedCallbackDelivered;
    private boolean completionDelivered;
    private int expectedDurationMs;
    private int durationMs;
    private int basePositionMs;
    private long basePositionClockMs;
    private long sourceGeneration;
    private long frameEpoch;
    private OnPreparedListener preparedListener;
    private OnCompletionListener completionListener;
    private AnimationEdits visualEdits = AnimationEdits.NONE;
    private Bitmap currentFrame;
    private Bitmap previousFrame;
    private ExoPlayer audioPlayer;
    private ExoPlayer musicPlayer;
    private Uri previewMusicUri;
    private float previewMusicVolume = 0.5f;
    private boolean previewMusicLoop = true;
    private long previewMusicStartMs;
    private long previewFadeMs;
    private long mixPositionMs;
    private long mixDurationMs;
    private long musicGeneration;
    private Consumer<String> audioStatusListener;
    private String audioStatus = "正在读取原声音轨…";
    private float previewVolume = 1f;
    private final Runnable audioTimeout = () -> fallbackAudio("原声准备超时，已切换为静音预览");

    void setAudioStatusListener(Consumer<String> listener) {
        audioStatusListener = listener;
        if (listener != null) listener.accept(audioStatus);
    }

    private void audioMessage(String message) {
        audioStatus = message;
        if (audioStatusListener != null) audioStatusListener.accept(message);
    }

    void setPreviewVolume(float volume) {
        previewVolume = Math.max(0f, Math.min(1f, volume));
        if (audioPlayer != null) {
            try { audioPlayer.setVolume(previewVolume); }
            catch (RuntimeException error) { fallbackAudio("原声预览暂不可用，可继续剪辑"); }
        }
    }


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

    private void prepareAudio(Uri source) {
        releaseAudio();
        if (detached || source == null) return;
        final long generation = sourceGeneration;
        try {
            ExoPlayer player = new ExoPlayer.Builder(getContext().getApplicationContext(),
                    new DefaultRenderersFactory(getContext().getApplicationContext())
                            .setEnableDecoderFallback(true))
                    .setLoadControl(new DefaultLoadControl.Builder()
                            .setBufferDurationsMs(1000, 5000, 250, 500).build())
                    .build();
            audioPlayer = player;
            player.setTrackSelectionParameters(player.getTrackSelectionParameters().buildUpon()
                    .setTrackTypeDisabled(C.TRACK_TYPE_VIDEO, true)
                    .setTrackTypeDisabled(C.TRACK_TYPE_TEXT, true)
                    .setTrackTypeDisabled(C.TRACK_TYPE_IMAGE, true)
                    .build());
            player.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(C.USAGE_MEDIA).setContentType(C.AUDIO_CONTENT_TYPE_MOVIE).build(), true);
            player.setHandleAudioBecomingNoisy(true);
            player.setVolume(previewVolume);
            player.addListener(new Player.Listener() {
                private boolean current() {
                    return !detached && sourceGeneration == generation && audioPlayer == player;
                }
                @Override public void onPlayerError(PlaybackException error) {
                    if (current()) fallbackAudio("此设备无法播放该原声，已切换为静音预览；仍可剪辑");
                }
                @Override public void onTracksChanged(Tracks tracks) {
                    if (!current() || tracks.isEmpty()) return;
                    if (!tracks.isTypeSelected(C.TRACK_TYPE_AUDIO)) {
                        String message = tracks.containsType(C.TRACK_TYPE_AUDIO)
                                ? "此音轨暂不支持，已切换为静音预览"
                                : "素材没有音轨，使用静音预览";
                        // Release outside of the event batch; source switches invalidate this task.
                        mainHandler.post(() -> { if (current()) fallbackAudio(message); });
                    }
                }
                @Override public void onPlaybackStateChanged(int state) {
                    if (!current()) return;
                    mainHandler.removeCallbacks(audioTimeout);
                    if (state == Player.STATE_BUFFERING) {
                        audioMessage("正在准备原声…");
                        mainHandler.postDelayed(audioTimeout, 8000L);
                    } else if (state == Player.STATE_READY) {
                        audioMessage("原声预览已就绪 · 音量随手机媒体音量调整");
                    } else if (state == Player.STATE_ENDED) {
                        // Some files have audio shorter than their video; finish the remaining images.
                        basePositionMs = clampPosition((int)Math.min(Integer.MAX_VALUE, player.getCurrentPosition()));
                        basePositionClockMs = SystemClock.elapsedRealtime();
                        mainHandler.post(() -> { if (current()) releaseAudio(); });
                    }
                }
                @Override public void onPlayWhenReadyChanged(boolean playWhenReady, int reason) {
                    if (current() && !playWhenReady && logicalPlaying
                            && (reason == Player.PLAY_WHEN_READY_CHANGE_REASON_AUDIO_FOCUS_LOSS
                            || reason == Player.PLAY_WHEN_READY_CHANGE_REASON_AUDIO_BECOMING_NOISY)) pause();
                }
                @Override public void onPlaybackSuppressionReasonChanged(int reason) {
                    if (current() && reason != Player.PLAYBACK_SUPPRESSION_REASON_NONE && logicalPlaying) pause();
                }
            });
            audioMessage("正在读取原声音轨…");
            player.setMediaItem(MediaItem.fromUri(source));
            player.prepare();
            mainHandler.postDelayed(audioTimeout, 8000L);
        } catch (RuntimeException | LinkageError error) {
            fallbackAudio("原声预览暂不可用，已切换为静音预览");
        }
    }

    private void fallbackAudio(String message) {
        // Retain the last known media position when switching to the image-only clock.
        if (audioPlayer != null) {
            try { basePositionMs = clampPosition((int)Math.min(Integer.MAX_VALUE, audioPlayer.getCurrentPosition())); }
            catch (RuntimeException ignored) { }
        }
        basePositionClockMs = SystemClock.elapsedRealtime();
        releaseAudio();
        audioMessage(message);
    }

    private void releaseAudio() {
        mainHandler.removeCallbacks(audioTimeout);
        ExoPlayer old = audioPlayer;
        audioPlayer = null; // Ignore queued callbacks from the released player.
        if (old != null) { try { old.release(); } catch (RuntimeException ignored) { } }
    }


    private final Runnable playbackTicker = new Runnable() {
        @Override public void run() {
            if (detached || !logicalPlaying) return;
            int position = calculatedPosition();
            if (durationMs > 0 && position >= durationMs) {
                finishPlayback();
                return;
            }
            requestFrame(position);
            mainHandler.postDelayed(this, FRAME_TICK_MS);
        }
    };

    EditorVideoPlayer(Context context) {
        super(context);
        renderer = new EditorPreviewRenderer(context.getApplicationContext());
        setBackgroundColor(0xFF111111);
        setClipChildren(true);
        setClipToPadding(true);

        frameView = new ImageView(context);
        frameView.setScaleType(ImageView.ScaleType.FIT_CENTER);
        frameView.setBackgroundColor(0xFF111111);
        frameView.setClickable(false);
        frameView.setFocusable(false);
        addView(frameView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));

        statusView = new TextView(context);
        statusView.setText("正在读取视频画面…");
        statusView.setTextColor(0xFFD7D8DE);
        statusView.setTextSize(12f);
        statusView.setGravity(Gravity.CENTER);
        statusView.setClickable(false);
        addView(statusView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT,
                Gravity.CENTER));
    }

    void setExpectedDurationMs(int milliseconds) {
        expectedDurationMs = Math.max(0, milliseconds);
        durationMs = expectedDurationMs;
        basePositionMs = clampPosition(basePositionMs);
        dispatchPreparedIfReady();
    }

    void setVideoURI(Uri value) {
        releaseAudio();
        sourceGeneration++;
        frameEpoch++;
        uri = value;
        basePositionMs = 0;
        basePositionClockMs = SystemClock.elapsedRealtime();
        durationMs = expectedDurationMs;
        preparedCallbackDelivered = false;
        completionDelivered = false;
        logicalPlaying = false;
        mainHandler.removeCallbacks(playbackTicker);

        frameView.setImageDrawable(null);
        recycle(previousFrame);
        recycle(currentFrame);
        previousFrame = null;
        currentFrame = null;
        statusView.setText("正在读取视频画面…");
        statusView.setVisibility(View.VISIBLE);
        requestFrame(0);
        prepareAudio(value);
        dispatchPreparedIfReady();
    }

    void setOnPreparedListener(OnPreparedListener listener) {
        preparedListener = listener;
        dispatchPreparedIfReady();
    }

    void setOnCompletionListener(OnCompletionListener listener) {
        completionListener = listener;
    }

    void seekTo(int milliseconds) {
        frameEpoch++;
        basePositionMs = clampPosition(Math.max(0, milliseconds));
        basePositionClockMs = SystemClock.elapsedRealtime();
        completionDelivered = false;
        if (audioPlayer != null) {
            try { audioPlayer.seekTo(basePositionMs); }
            catch (RuntimeException error) { fallbackAudio("定位原声失败，已切换为静音预览"); }
        }
        requestFrame(basePositionMs);
        if (logicalPlaying) schedulePlaybackTicker();
    }

    void start() {
        if (detached) return;
        int position = calculatedPosition();
        if (durationMs > 0 && position >= Math.max(0, durationMs - 1)) position = 0;
        basePositionMs = position;
        basePositionClockMs = SystemClock.elapsedRealtime();
        completionDelivered = false;
        logicalPlaying = true;
        if (audioPlayer != null) {
            try {
                audioPlayer.seekTo(position);
                audioPlayer.play();
            } catch (RuntimeException error) { fallbackAudio("播放原声失败，已切换为静音预览"); }
        }
        syncMusic(true);
        requestFrame(position);
        schedulePlaybackTicker();
    }

    void pause() {
        basePositionMs = calculatedPosition();
        basePositionClockMs = SystemClock.elapsedRealtime();
        logicalPlaying = false;
        mainHandler.removeCallbacks(playbackTicker);
        if (audioPlayer != null) {
            try { audioPlayer.pause(); }
            catch (RuntimeException error) { fallbackAudio("原声预览暂不可用，可继续剪辑"); }
        }
        if (musicPlayer != null) {
            try { musicPlayer.pause(); } catch (RuntimeException error) { releaseMusic(); }
        }
        requestFrame(basePositionMs);
    }

    boolean isPlaying() {
        return logicalPlaying;
    }

    int getDuration() {
        return Math.max(0, durationMs > 0 ? durationMs : expectedDurationMs);
    }

    int getCurrentPosition() {
        return calculatedPosition();
    }

    void applyVisualEdits(AnimationEdits edits) {
        frameEpoch++;
        visualEdits = edits == null ? AnimationEdits.NONE : edits;
        requestFrame(calculatedPosition());
    }

    private void dispatchPreparedIfReady() {
        if (preparedCallbackDelivered || preparedListener == null
                || uri == null || getDuration() <= 0) return;
        preparedCallbackDelivered = true;
        final long generation = sourceGeneration;
        mainHandler.post(() -> {
            if (!detached && generation == sourceGeneration && preparedListener != null) preparedListener.onPrepared(this);
        });
    }

    private int calculatedPosition() {
        if (audioPlayer != null) {
            try {
                basePositionMs = clampPosition((int)Math.min(Integer.MAX_VALUE, audioPlayer.getCurrentPosition()));
                basePositionClockMs = SystemClock.elapsedRealtime();
                return basePositionMs;
            } catch (RuntimeException error) { fallbackAudio("原声预览中断，已切换为静音预览"); }
        }
        long value = basePositionMs;
        if (logicalPlaying) {
            value += Math.max(0L, SystemClock.elapsedRealtime() - basePositionClockMs);
        }
        if (durationMs > 0) value = Math.min(durationMs, value);
        return (int) Math.max(0L, Math.min(Integer.MAX_VALUE, value));
    }

    private int clampPosition(int value) {
        if (durationMs <= 0) return Math.max(0, value);
        return Math.max(0, Math.min(durationMs, value));
    }

    private void schedulePlaybackTicker() {
        mainHandler.removeCallbacks(playbackTicker);
        if (logicalPlaying && !detached) mainHandler.post(playbackTicker);
    }

    private void finishPlayback() {
        basePositionMs = Math.max(0, durationMs);
        basePositionClockMs = SystemClock.elapsedRealtime();
        logicalPlaying = false;
        mainHandler.removeCallbacks(playbackTicker);
        if (audioPlayer != null) {
            try { audioPlayer.pause(); } catch (RuntimeException ignored) { releaseAudio(); }
        }
        if (musicPlayer != null) {
            try { musicPlayer.pause(); } catch (RuntimeException ignored) { releaseMusic(); }
        }
        requestFrame(Math.max(0, durationMs - 1));
        if (!completionDelivered) {
            completionDelivered = true;
            if (completionListener != null) completionListener.onCompletion(this);
        }
    }

    private void requestFrame(int positionMs) {
        Uri requestedUri = uri;
        if (requestedUri == null || detached) return;
        final long generation = sourceGeneration;
        final long requestedEpoch = frameEpoch;
        int width = Math.max(160, getWidth());
        int height = Math.max(100, getHeight());
        try {
            renderer.request(requestedUri, Math.max(0, positionMs), visualEdits,
                    width, height, bitmap -> mainHandler.post(() -> {
                        if (detached || generation != sourceGeneration
                                || requestedEpoch != frameEpoch) {
                            recycle(bitmap);
                            return;
                        }
                        showFrame(bitmap);
                    }));
        } catch (Throwable ignored) {
            // A preview decoder failure must never stop the editor controls from opening/working.
        }
    }

    private void showFrame(Bitmap bitmap) {
        if (bitmap == null || bitmap.isRecycled()) return;
        Bitmap stale = previousFrame;
        previousFrame = currentFrame;
        currentFrame = bitmap;
        frameView.setImageBitmap(bitmap);
        statusView.setVisibility(View.GONE);
        recycle(stale);
    }

    void stopPlayback() {
        // Dialog dismissal is terminal; prevent late frame/track callbacks and free codecs now.
        detached = true;
        logicalPlaying = false;
        releaseAudio();
        releaseMusic();
        mainHandler.removeCallbacksAndMessages(null);
        renderer.close();
    }

    @Override
    protected void onSizeChanged(int width, int height, int oldWidth, int oldHeight) {
        super.onSizeChanged(width, height, oldWidth, oldHeight);
        requestFrame(calculatedPosition());
    }

    @Override
    protected void onDetachedFromWindow() {
        detached = true;
        logicalPlaying = false;
        releaseAudio();
        releaseMusic();
        audioStatusListener = null;
        mainHandler.removeCallbacksAndMessages(null);
        renderer.close();
        frameView.setImageDrawable(null);
        recycle(previousFrame);
        recycle(currentFrame);
        previousFrame = null;
        currentFrame = null;
        super.onDetachedFromWindow();
    }

    private static void recycle(Bitmap bitmap) {
        if (bitmap != null && !bitmap.isRecycled()) {
            try { bitmap.recycle(); } catch (Throwable ignored) { }
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/EglBitmapRenderer.java': r'''package com.qi.formatconverter;

import android.graphics.Bitmap;
import android.opengl.EGL14;
import android.opengl.EGLExt;
import android.opengl.GLES20;
import android.opengl.GLUtils;
import android.view.Surface;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;

final class EglBitmapRenderer implements AutoCloseable {
    private static final String VERTEX_SHADER =
            "attribute vec4 aPosition;\n" +
            "attribute vec2 aTexCoord;\n" +
            "varying vec2 vTexCoord;\n" +
            "void main() {\n" +
            "  gl_Position = aPosition;\n" +
            "  vTexCoord = aTexCoord;\n" +
            "}\n";

    private static final String FRAGMENT_SHADER =
            "precision mediump float;\n" +
            "uniform sampler2D uTexture;\n" +
            "varying vec2 vTexCoord;\n" +
            "void main() {\n" +
            "  gl_FragColor = texture2D(uTexture, vTexCoord);\n" +
            "}\n";

    private final Surface inputSurface;
    private android.opengl.EGLDisplay display = EGL14.EGL_NO_DISPLAY;
    private android.opengl.EGLContext context = EGL14.EGL_NO_CONTEXT;
    private android.opengl.EGLSurface eglSurface = EGL14.EGL_NO_SURFACE;
    private int program;
    private int textureId;
    private int positionLoc;
    private int texCoordLoc;
    private int textureLoc;
    private final int outputWidth;
    private final int outputHeight;
    private final FloatBuffer vertexBuffer = allocateFloatBuffer(8);
    private final FloatBuffer textureBuffer = createFloatBuffer(new float[]{
            0f, 1f,
            1f, 1f,
            0f, 0f,
            1f, 0f
    });
    private int uploadedWidth = -1;
    private int uploadedHeight = -1;

    EglBitmapRenderer(Surface inputSurface, int outputWidth, int outputHeight) {
        this.inputSurface = inputSurface;
        this.outputWidth = outputWidth;
        this.outputHeight = outputHeight;
        try {
            setupEgl();
            setupGl();
        } catch (Throwable error) {
            releaseEglResources();
            throw error;
        }
    }

    private void setupEgl() {
        display = EGL14.eglGetDisplay(EGL14.EGL_DEFAULT_DISPLAY);
        if (display == EGL14.EGL_NO_DISPLAY) {
            throw new RuntimeException("无法取得 EGLDisplay");
        }
        int[] version = new int[2];
        if (!EGL14.eglInitialize(display, version, 0, version, 1)) {
            throw new RuntimeException("无法初始化 EGL");
        }

        int[] attribList = {
                EGL14.EGL_RED_SIZE, 8,
                EGL14.EGL_GREEN_SIZE, 8,
                EGL14.EGL_BLUE_SIZE, 8,
                EGL14.EGL_ALPHA_SIZE, 8,
                EGL14.EGL_RENDERABLE_TYPE, EGL14.EGL_OPENGL_ES2_BIT,
                0x3142, 1,
                EGL14.EGL_NONE
        };
        android.opengl.EGLConfig[] configs = new android.opengl.EGLConfig[1];
        int[] numConfigs = new int[1];
        if (!EGL14.eglChooseConfig(display, attribList, 0, configs, 0, 1, numConfigs, 0)
                || numConfigs[0] <= 0) {
            throw new RuntimeException("找不到可用 EGLConfig");
        }

        int[] contextAttribs = {
                EGL14.EGL_CONTEXT_CLIENT_VERSION, 2,
                EGL14.EGL_NONE
        };
        context = EGL14.eglCreateContext(
                display, configs[0], EGL14.EGL_NO_CONTEXT, contextAttribs, 0);
        checkEgl("eglCreateContext");

        int[] surfaceAttribs = {EGL14.EGL_NONE};
        eglSurface = EGL14.eglCreateWindowSurface(
                display, configs[0], inputSurface, surfaceAttribs, 0);
        checkEgl("eglCreateWindowSurface");

        if (!EGL14.eglMakeCurrent(display, eglSurface, eglSurface, context)) {
            throw new RuntimeException("eglMakeCurrent 失败");
        }
    }

    private void setupGl() {
        program = createProgram(VERTEX_SHADER, FRAGMENT_SHADER);
        positionLoc = GLES20.glGetAttribLocation(program, "aPosition");
        texCoordLoc = GLES20.glGetAttribLocation(program, "aTexCoord");
        textureLoc = GLES20.glGetUniformLocation(program, "uTexture");

        int[] textures = new int[1];
        GLES20.glGenTextures(1, textures, 0);
        textureId = textures[0];
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureId);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_LINEAR);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE);
    }

    void draw(Bitmap bitmap, long presentationTimeNs) {
        float sourceAspect = bitmap.getWidth() / (float) bitmap.getHeight();
        float outputAspect = outputWidth / (float) outputHeight;
        float x = 1f;
        float y = 1f;
        if (sourceAspect > outputAspect) {
            y = outputAspect / sourceAspect;
        } else {
            x = sourceAspect / outputAspect;
        }

        vertexBuffer.clear();
        vertexBuffer.put(-x).put(-y);
        vertexBuffer.put(x).put(-y);
        vertexBuffer.put(-x).put(y);
        vertexBuffer.put(x).put(y);
        vertexBuffer.position(0);
        textureBuffer.position(0);

        GLES20.glViewport(0, 0, outputWidth, outputHeight);
        GLES20.glClearColor(0f, 0f, 0f, 1f);
        GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT);
        GLES20.glUseProgram(program);

        GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureId);
        if (uploadedWidth != bitmap.getWidth() || uploadedHeight != bitmap.getHeight()) {
            GLUtils.texImage2D(GLES20.GL_TEXTURE_2D, 0, bitmap, 0);
            uploadedWidth = bitmap.getWidth();
            uploadedHeight = bitmap.getHeight();
        } else {
            GLUtils.texSubImage2D(GLES20.GL_TEXTURE_2D, 0, 0, 0, bitmap);
        }
        GLES20.glUniform1i(textureLoc, 0);

        GLES20.glEnableVertexAttribArray(positionLoc);
        GLES20.glVertexAttribPointer(positionLoc, 2, GLES20.GL_FLOAT, false, 0, vertexBuffer);
        GLES20.glEnableVertexAttribArray(texCoordLoc);
        GLES20.glVertexAttribPointer(
                texCoordLoc, 2, GLES20.GL_FLOAT, false, 0, textureBuffer);
        GLES20.glDrawArrays(GLES20.GL_TRIANGLE_STRIP, 0, 4);
        GLES20.glDisableVertexAttribArray(positionLoc);
        GLES20.glDisableVertexAttribArray(texCoordLoc);

        EGLExt.eglPresentationTimeANDROID(display, eglSurface, presentationTimeNs);
        if (!EGL14.eglSwapBuffers(display, eglSurface)) {
            throw new RuntimeException("eglSwapBuffers 失败");
        }
    }

    private static FloatBuffer allocateFloatBuffer(int count) {
        return ByteBuffer.allocateDirect(count * 4)
                .order(ByteOrder.nativeOrder())
                .asFloatBuffer();
    }

    private static FloatBuffer createFloatBuffer(float[] values) {
        FloatBuffer buffer = allocateFloatBuffer(values.length);
        buffer.put(values).position(0);
        return buffer;
    }

    private static int createProgram(String vertex, String fragment) {
        int vertexShader = loadShader(GLES20.GL_VERTEX_SHADER, vertex);
        int fragmentShader = loadShader(GLES20.GL_FRAGMENT_SHADER, fragment);
        int program = GLES20.glCreateProgram();
        GLES20.glAttachShader(program, vertexShader);
        GLES20.glAttachShader(program, fragmentShader);
        GLES20.glLinkProgram(program);
        int[] linked = new int[1];
        GLES20.glGetProgramiv(program, GLES20.GL_LINK_STATUS, linked, 0);
        if (linked[0] == 0) {
            String log = GLES20.glGetProgramInfoLog(program);
            GLES20.glDeleteProgram(program);
            throw new RuntimeException("OpenGL 程序链接失败：" + log);
        }
        GLES20.glDeleteShader(vertexShader);
        GLES20.glDeleteShader(fragmentShader);
        return program;
    }

    private static int loadShader(int type, String source) {
        int shader = GLES20.glCreateShader(type);
        GLES20.glShaderSource(shader, source);
        GLES20.glCompileShader(shader);
        int[] compiled = new int[1];
        GLES20.glGetShaderiv(shader, GLES20.GL_COMPILE_STATUS, compiled, 0);
        if (compiled[0] == 0) {
            String log = GLES20.glGetShaderInfoLog(shader);
            GLES20.glDeleteShader(shader);
            throw new RuntimeException("OpenGL 着色器编译失败：" + log);
        }
        return shader;
    }

    private void checkEgl(String operation) {
        int error = EGL14.eglGetError();
        if (error != EGL14.EGL_SUCCESS) {
            throw new RuntimeException(operation + " EGL 错误 0x" + Integer.toHexString(error));
        }
    }

    @Override
    public void close() {
        releaseEglResources();
        inputSurface.release();
    }

    private void releaseEglResources() {
        if (display != EGL14.EGL_NO_DISPLAY) {
            if (program != 0) {
                GLES20.glDeleteProgram(program);
                program = 0;
            }
            if (textureId != 0) {
                GLES20.glDeleteTextures(1, new int[]{textureId}, 0);
                textureId = 0;
            }
            EGL14.eglMakeCurrent(
                    display,
                    EGL14.EGL_NO_SURFACE,
                    EGL14.EGL_NO_SURFACE,
                    EGL14.EGL_NO_CONTEXT);
            if (eglSurface != EGL14.EGL_NO_SURFACE) {
                EGL14.eglDestroySurface(display, eglSurface);
            }
            if (context != EGL14.EGL_NO_CONTEXT) {
                EGL14.eglDestroyContext(display, context);
            }
            EGL14.eglReleaseThread();
            EGL14.eglTerminate(display);
        }
        display = EGL14.EGL_NO_DISPLAY;
        context = EGL14.EGL_NO_CONTEXT;
        eglSurface = EGL14.EGL_NO_SURFACE;
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/ExtraImageFormats.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.RectF;
import android.net.Uri;
import android.provider.OpenableColumns;
import com.caverock.androidsvg.SVG;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.zip.*;

/** Bounded readers and streaming writers for portable raster formats; static SVG rasterization. */
final class ExtraImageFormats {
    private ExtraImageFormats() { }
    static String kind(Context c, Uri uri) {
        String mime=c.getContentResolver().getType(uri),name=uri.getLastPathSegment();
        if(mime!=null&&Arrays.asList("image/jpeg","image/png","image/gif","image/webp","image/heif","image/heic","image/avif","image/bmp").contains(mime))return "";
        try(Cursor cursor=c.getContentResolver().query(uri,new String[]{OpenableColumns.DISPLAY_NAME},null,null,null)) {
            if(cursor!=null&&cursor.moveToFirst())name=cursor.getString(0);
        }catch(Exception ignored){}
        name=name==null?"":name.toLowerCase(Locale.ROOT);
        if(name.matches(".*\\.(tif|tiff)$")||"image/tiff".equals(mime))return "TIFF";
        if(name.matches(".*\\.(ppm|pgm|pbm|pnm|pam)$")||(mime!=null&&mime.contains("portable-")))return "PNM";
        if(name.endsWith(".tga")||"image/x-tga".equals(mime))return "TGA";
        if(name.endsWith(".svg")||name.endsWith(".svgz")||"image/svg+xml".equals(mime))return "SVG";
        return "";
    }
    static Bitmap decode(Context c,Uri uri,String kind,int maxWidth,int maxHeight,long pixelCap)throws IOException {
        if("SVG".equals(kind))return svg(c,uri,maxWidth,maxHeight,pixelCap);
        // The sampled int buffer and Bitmap briefly coexist. Budget for both.
        pixelCap=Math.max(1,pixelCap/2);
        if("TIFF".equals(kind)) {
            File file=File.createTempFile("image_",".tif",c.getCacheDir());
            try {
                DocumentKit.copy(c,uri,file,512L*1024*1024,ExtraImageFormats::check);
                try(RandomAccessFile input=new RandomAccessFile(file,"r")){return tiff(input,maxWidth,maxHeight,pixelCap).bitmap();}
            }catch(IOException e){throw e;}catch(Exception e){throw new IOException(e.getMessage(),e);}finally{file.delete();}
        }
        try(InputStream raw=c.getContentResolver().openInputStream(uri)) {
            if(raw==null)throw new IOException("无法读取图片");
            PushbackInputStream input=new PushbackInputStream(new BufferedInputStream(raw,65536),2);
            return ("TGA".equals(kind)?tga(input,maxWidth,maxHeight,pixelCap):pnm(input,maxWidth,maxHeight,pixelCap)).bitmap();
        }
    }
    static final class Raster {
        final int sourceWidth,sourceHeight,width,height;
        final int[] pixels;
        Raster(int w,int h,int maxW,int maxH,long cap)throws IOException {this(w,h,maxW,maxH,cap,true);}
        Raster(int w,int h,int maxW,int maxH,long cap,boolean allocate)throws IOException {
            if(w<=0||h<=0||w>100000||h>100000||(long)w*h>100_000_000)throw new IOException("图片尺寸超出安全范围（最多 1 亿像素）");
            sourceWidth=w;sourceHeight=h;double scale=Math.min(1,Math.min(maxW/(double)w,maxH/(double)h));
            scale=Math.min(scale,Math.sqrt(Math.max(1,cap)/(double)((long)w*h)));
            width=Math.max(1,(int)Math.floor(w*scale));height=Math.max(1,(int)Math.floor(h*scale));pixels=allocate?new int[width*height]:null;
        }
        // Select one exact source pixel for each output cell. Never allocate a full-size source image.
        void put(int x,int y,int argb) {
            int ox=(int)((long)x*width/sourceWidth),oy=(int)((long)y*height/sourceHeight);
            if(x==(int)(((long)ox*sourceWidth+width-1)/width)&&y==(int)(((long)oy*sourceHeight+height-1)/height))pixels[oy*width+ox]=argb;
        }
        Bitmap bitmap(){return Bitmap.createBitmap(pixels,width,height,Bitmap.Config.ARGB_8888);}
    }
    static Raster pnm(PushbackInputStream in,int maxW,int maxH,long cap)throws IOException {
        String magic=token(in);int type=magic.length()==2&&magic.charAt(0)=='P'?magic.charAt(1)-'0':0;
        if(type<1||type>7)throw new IOException("不是 PNM/PAM 图片");
        int w,h,max=1,depth=0;
        if(type==7){Map<String,String> fields=new HashMap<>();String key;while(!(key=token(in)).equals("ENDHDR")){if(fields.size()>20)throw new IOException("PAM 头部无效");fields.put(key,token(in));}w=number(fields.get("WIDTH"));h=number(fields.get("HEIGHT"));max=number(fields.get("MAXVAL"));depth=number(fields.get("DEPTH"));String tuple=fields.get("TUPLTYPE");if(depth<1||depth>4||(tuple!=null&&!Arrays.asList("RGB","RGB_ALPHA","GRAYSCALE","GRAYSCALE_ALPHA","BLACKANDWHITE","BLACKANDWHITE_ALPHA").contains(tuple)))throw new IOException("不支持此 PAM 通道类型");}
        else{w=number(token(in));h=number(token(in));if(type!=1&&type!=4)max=number(token(in));depth=(type==3||type==6)?3:1;}
        if(max<1||max>65535)throw new IOException("PNM 位深无效");
        Raster raster=new Raster(w,h,maxW,maxH,cap);boolean ascii=type<=3;int packed=0;
        for(int y=0;y<h;y++){check();for(int x=0;x<w;x++){
            int r,g,b,a=255;
            if(type==4){if(x%8==0)packed=read(in);r=g=b=((packed>>(7-x%8))&1)==1?0:255;}
            else if(type==1){int bit=number(token(in));if(bit>1)throw new IOException("PBM 像素无效");r=g=b=bit==1?0:255;}
            else{r=value(in,ascii,max);if(depth>=3){g=value(in,ascii,max);b=value(in,ascii,max);}else g=b=r;if(depth==2||depth==4)a=value(in,ascii,max);}
            raster.put(x,y,(a<<24)|(r<<16)|(g<<8)|b);
        }}return raster;
    }
    private static int value(InputStream in,boolean ascii,int max)throws IOException{int value=ascii?number(token((PushbackInputStream)in)):max>255?(read(in)<<8)|read(in):read(in);if(value<0||value>max)throw new IOException("PNM 像素超出范围");return (int)((value*255L+max/2)/max);}
    private static int number(String s)throws IOException{try{int n=Integer.parseInt(s);if(n<0)throw new NumberFormatException();return n;}catch(Exception e){throw new IOException("图片头部数值无效");}}
    private static String token(PushbackInputStream in)throws IOException {
        int c;while(true){c=read(in);if(c=='#'){while(c!='\n'&&c!='\r')c=read(in);continue;}if(c>32)break;}
        StringBuilder b=new StringBuilder();while(c>32&&c!='#'){if(b.length()>100)throw new IOException("图片头部过长");b.append((char)c);c=in.read();}
        if(c=='#'){while(c!='\n'&&c!='\r')c=read(in);}
        if(c=='\r'){int n=in.read();if(n>=0&&n!='\n')in.unread(n);}
        return b.toString();
    }
    static Raster tga(InputStream in,int maxW,int maxH,long cap)throws IOException {
        byte[] header=new byte[18];fully(in,header);
        int id=header[0]&255,map=header[1]&255,type=header[2]&255,w=u16(header,12),h=u16(header,14),bits=header[16]&255,descriptor=header[17]&255;
        if(map!=0||!(type==2||type==3||type==10||type==11)||(descriptor&0xc0)!=0)throw new IOException("TGA 支持真彩色/灰度及 RLE，不支持调色板/交错版本");
        boolean gray=type==3||type==11,rle=type>=10;
        if(gray?bits!=8&&bits!=16:bits!=16&&bits!=24&&bits!=32)throw new IOException("TGA 位深不支持");
        for(int i=0;i<id;i++)read(in);Raster raster=new Raster(w,h,maxW,maxH,cap);int count=w*h,done=0;
        while(done<count){check();int packet=rle?read(in):0,run=rle?(packet&127)+1:1;if(run>count-done)throw new IOException("TGA RLE 长度越界");boolean repeated=rle&&(packet&128)!=0;int color=0;
            for(int n=0;n<run;n++){if(n==0||!repeated){int b=read(in),g,r,a=255;if(gray){g=r=b;if(bits==16)a=read(in);}else if(bits==16){int v=b|(read(in)<<8);b=(v&31)*255/31;g=((v>>5)&31)*255/31;r=((v>>10)&31)*255/31;if((descriptor&15)>0)a=(v&0x8000)==0?0:255;}else{g=read(in);r=read(in);if(bits==32){int alpha=read(in);if((descriptor&15)>0)a=alpha;}}color=(a<<24)|(r<<16)|(g<<8)|b;}
                int x=done%w,y=done/w;if((descriptor&16)!=0)x=w-1-x;if((descriptor&32)==0)y=h-1-y;raster.put(x,y,color);done++;
            }
        }return raster;
    }
    static Raster tiff(RandomAccessFile in,int maxW,int maxH,long cap)throws IOException {
        int a=in.readUnsignedByte(),b=in.readUnsignedByte();boolean le=a=='I'&&b=='I';if(!le&&!(a=='M'&&b=='M'))throw new IOException("TIFF 字节序无效");
        if(shortAt(in,le)!=42)throw new IOException("暂不支持 BigTIFF");long ifd=intAt(in,le);if(ifd<8||ifd>in.length()-2)throw new IOException("TIFF 目录无效");in.seek(ifd);int count=shortAt(in,le);if(count>1024)throw new IOException("TIFF 标签过多");Map<Integer,long[]> tags=new HashMap<>();int totalValues=0;
        for(int i=0;i<count;i++){int tag=shortAt(in,le),type=shortAt(in,le);long n=intAt(in,le),valuePos=in.getFilePointer();long value=intAt(in,le),next=in.getFilePointer();if(n>100000)throw new IOException("TIFF 标签过大");int size=type==3?2:type==4?4:type==1?1:0;if(size>0&&Arrays.asList(256,257,258,259,262,273,274,277,278,279,284,317,322,323,338,339).contains(tag)){totalValues+=(int)n;if(totalValues>200000)throw new IOException("TIFF 目录内存超出限制");long pos=n*size<=4?valuePos:value;if(pos<0||pos+n*size>in.length())throw new IOException("TIFF 标签越界");in.seek(pos);long[] values=new long[(int)n];for(int j=0;j<n;j++)values[j]=size==1?in.readUnsignedByte():size==2?shortAt(in,le):intAt(in,le);tags.put(tag,values);}in.seek(next);}
        int w=(int)tag(tags,256,0),h=(int)tag(tags,257,0),channels=(int)tag(tags,277,1),compression=(int)tag(tags,259,1),photo=(int)tag(tags,262,2),rows=(int)Math.min(h,tag(tags,278,h)),predictor=(int)tag(tags,317,1);
        if(tag(tags,284,1)!=1||tag(tags,274,1)!=1||tags.containsKey(322)||tags.containsKey(323))throw new IOException("TIFF 暂支持左上原点、连续通道、条带布局；不支持分平面/瓦片布局");
        if((photo!=0&&photo!=1&&photo!=2)||(photo==2?channels!=3&&channels!=4:channels!=1&&channels!=2))throw new IOException("TIFF 暂支持灰度 / RGB / RGBA，不支持 CMYK / YCbCr");
        long[] bits=tags.get(258);if(bits==null)bits=new long[]{1};for(long bit:bits)if(bit!=8)throw new IOException("TIFF 当前读取支持每通道 8 bit");
        if(compression!=1&&compression!=8&&compression!=32946&&compression!=32773&&compression!=5)throw new IOException("TIFF 不支持此压缩方式；支持未压缩 / Deflate / PackBits / LZW");
        if(rows<=0||(predictor!=1&&predictor!=2)||tag(tags,339,1)!=1)throw new IOException("TIFF 数据类型不支持");
        long[] offsets=tags.get(273),sizes=tags.get(279);if(offsets==null||sizes==null||offsets.length!=sizes.length||offsets.length!=(h+(long)rows-1)/rows)throw new IOException("TIFF 条带目录不完整");
        Raster raster=new Raster(w,h,maxW,maxH,cap);int y=0,rowBytes=w*channels;boolean associated=tag(tags,338,2)==1;
        for(int strip=0;strip<offsets.length;strip++){check();int lines=Math.min(rows,h-y);long expected=(long)rowBytes*lines;if(expected>64L*1024*1024||sizes[strip]>64L*1024*1024||sizes[strip]<0||offsets[strip]<0||offsets[strip]+sizes[strip]>in.length())throw new IOException("TIFF 单条带超过 64 MB 或条带越界，请重新保存为较小条带");
            in.seek(offsets[strip]);byte[] packed=new byte[(int)sizes[strip]];in.readFully(packed);byte[] bytes;
            if(compression==1){if(packed.length<expected)throw new IOException("TIFF 条带不完整");bytes=packed;}
            else if(compression==8||compression==32946){bytes=new byte[(int)expected];try(InputStream z=new InflaterInputStream(new ByteArrayInputStream(packed))){fully(z,bytes);if(z.read()!=-1)throw new IOException("TIFF 条带解压大小不符");}}
            else if(compression==5)bytes=lzw(packed,(int)expected);
            else bytes=packBits(packed,(int)expected);
            for(int row=0;row<lines;row++,y++){check();int base=row*rowBytes;if(predictor==2)for(int x=channels;x<rowBytes;x++)bytes[base+x]=(byte)((bytes[base+x]&255)+(bytes[base+x-channels]&255));
                for(int x=0;x<w;x++){int p=base+x*channels,r=bytes[p]&255,g=r,blue=r,alpha=255;if(photo==0)r=g=blue=255-r;if(photo==2){g=bytes[p+1]&255;blue=bytes[p+2]&255;if(channels==4)alpha=bytes[p+3]&255;}else if(channels==2)alpha=bytes[p+1]&255;if(associated&&alpha>0){r=Math.min(255,r*255/alpha);g=Math.min(255,g*255/alpha);blue=Math.min(255,blue*255/alpha);}raster.put(x,y,(alpha<<24)|(r<<16)|(g<<8)|blue);}
            }
        }return raster;
    }
    private static long tag(Map<Integer,long[]> tags,int key,long fallback){long[] values=tags.get(key);return values==null||values.length==0?fallback:values[0];}
    static byte[] packBits(byte[] data,int expected)throws IOException {byte[] out=new byte[expected];int p=0,o=0;while(p<data.length&&o<expected){int n=data[p++];if(n>=0){int count=n+1;if(p+count>data.length||o+count>expected)throw new IOException("PackBits 数据损坏");System.arraycopy(data,p,out,o,count);p+=count;o+=count;}else if(n!=-128){int count=1-n;if(p>=data.length||o+count>expected)throw new IOException("PackBits 数据损坏");Arrays.fill(out,o,o+count,data[p++]);o+=count;}}if(o!=expected)throw new IOException("PackBits 数据不完整");return out;}
    static byte[] lzw(byte[] data,int expected)throws IOException {
        byte[] out=new byte[expected],stack=new byte[4096];int[] prefix=new int[4096];byte[] suffix=new byte[4096];for(int i=0;i<256;i++)suffix[i]=(byte)i;
        int bits=9,next=258,previous=-1,first=0,bit=0,position=0;
        while(bit+bits<=data.length*8){check();int code=0;for(int i=0;i<bits;i++,bit++)code=(code<<1)|((data[bit/8]>>(7-bit%8))&1);if(code==257)break;if(code==256){bits=9;next=258;previous=-1;continue;}int original=code,top=0;if(code==next&&previous>=0){stack[top++]=(byte)first;code=previous;}else if(code>=next)throw new IOException("TIFF LZW 字典无效");
            while(code>=256){if(code>=next||top>=4095)throw new IOException("TIFF LZW 字典循环");stack[top++]=suffix[code];code=prefix[code];}first=code;stack[top++]=(byte)first;if(position+top>expected)throw new IOException("TIFF LZW 解压越界");while(top>0)out[position++]=stack[--top];if(previous>=0&&next<4096){prefix[next]=previous;suffix[next]=(byte)first;next++;if(next==(1<<bits)-1&&bits<12)bits++;}previous=original;
        }if(position!=expected)throw new IOException("TIFF LZW 数据不完整");return out;
    }
    private static Bitmap svg(Context c,Uri uri,int maxW,int maxH,long cap)throws IOException {
        try(InputStream raw=c.getContentResolver().openInputStream(uri)) {
            if(raw==null)throw new IOException("无法读取 SVG");PushbackInputStream probe=new PushbackInputStream(raw,2);int a=probe.read(),b=probe.read();if(b>=0)probe.unread(b);if(a>=0)probe.unread(a);
            InputStream in=a==31&&b==139?new GZIPInputStream(probe):probe;
            ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buffer=new byte[8192];int n;
            while((n=in.read(buffer))!=-1){check();if(bytes.size()+n>4*1024*1024)throw new IOException("SVG 解压后超过 4 MB");bytes.write(buffer,0,n);}
            String source=new String(bytes.toByteArray(),StandardCharsets.UTF_8),upper=source.toUpperCase(Locale.ROOT);
            if(upper.contains("<!DOCTYPE")||upper.contains("<!ENTITY")||source.matches("(?is).*<(?:\\w+:)?(?:script|image|filter|foreignObject|animate|animateTransform|animateMotion)\\b.*"))throw new IOException("SVG 支持静态矢量；请去除脚本、外部图像、滤镜、动画或 DTD 后再转换");
            if(source.matches("(?is).*\\b(?:href|xlink:href)\\s*=\\s*['\"](?!#)[^'\"]+['\"].*"))throw new IOException("SVG 不支持外部资源链接");
            SVG svg=SVG.getFromString(source);float w=svg.getDocumentWidth(),h=svg.getDocumentHeight();RectF box=svg.getDocumentViewBox();if(w<=0&&box!=null)w=box.width();if(h<=0&&box!=null)h=box.height();if(w<=0)w=512;if(h<=0)h=512;
            Raster raster=new Raster((int)Math.ceil(w),(int)Math.ceil(h),maxW,maxH,cap,false);Bitmap bitmap=Bitmap.createBitmap(raster.width,raster.height,Bitmap.Config.ARGB_8888);
            svg.setDocumentWidth(raster.width);svg.setDocumentHeight(raster.height);svg.renderToCanvas(new Canvas(bitmap));return bitmap;
        }catch(IOException e){throw e;}catch(Exception e){throw new IOException("SVG 无法解析："+e.getMessage(),e);}
    }
    static void write(Bitmap bitmap,int format,OutputStream out)throws IOException {
        int w=bitmap.getWidth(),h=bitmap.getHeight();int[] row=new int[w];byte[] bytes=new byte[Math.max(w*4,(w+7)/8)];
        if(format==29){int entries=12,strips=(h+63)/64,bitsOffset=8+2+entries*12+4,offsets=bitsOffset+8,sizes=offsets+strips*4,dataOffset=strips==1?offsets:sizes+strips*4;
            out.write('I');out.write('I');le16(out,42);le32(out,8);le16(out,entries);entry(out,256,4,1,w);entry(out,257,4,1,h);entry(out,258,3,4,bitsOffset);entry(out,259,3,1,1);entry(out,262,3,1,2);entry(out,273,4,strips,strips==1?dataOffset:offsets);entry(out,274,3,1,1);entry(out,277,3,1,4);entry(out,278,4,1,64);entry(out,279,4,strips,strips==1?(long)w*h*4:sizes);entry(out,284,3,1,1);entry(out,338,3,1,2);le32(out,0);for(int i=0;i<4;i++)le16(out,8);
            if(strips>1){for(int i=0;i<strips;i++)le32(out,dataOffset+(long)i*64*w*4);for(int i=0;i<strips;i++)le32(out,(long)Math.min(64,h-i*64)*w*4);}
        }
        else if(format==30){if(w>65535||h>65535)throw new IOException("TGA 尺寸过大");byte[] header=new byte[18];header[2]=2;header[12]=(byte)w;header[13]=(byte)(w>>8);header[14]=(byte)h;header[15]=(byte)(h>>8);header[16]=32;header[17]=40;out.write(header);}
        else{String header=format==31?"P6\n"+w+" "+h+"\n255\n":format==32?"P5\n"+w+" "+h+"\n255\n":format==33?"P4\n"+w+" "+h+"\n":"P7\nWIDTH "+w+"\nHEIGHT "+h+"\nDEPTH 4\nMAXVAL 255\nTUPLTYPE RGB_ALPHA\nENDHDR\n";out.write(header.getBytes(StandardCharsets.US_ASCII));}
        for(int y=0;y<h;y++){check();bitmap.getPixels(row,0,w,0,y,w,1);int p=0;Arrays.fill(bytes,(byte)0);
            for(int x=0;x<w;x++){int c=row[x],a=c>>>24,r=(c>>16)&255,g=(c>>8)&255,b=c&255;
                if(format==29||format==34){bytes[p++]=(byte)r;bytes[p++]=(byte)g;bytes[p++]=(byte)b;bytes[p++]=(byte)a;}
                else if(format==30){bytes[p++]=(byte)b;bytes[p++]=(byte)g;bytes[p++]=(byte)r;bytes[p++]=(byte)a;}
                else{r=(r*a+255*(255-a)+127)/255;g=(g*a+255*(255-a)+127)/255;b=(b*a+255*(255-a)+127)/255;
                    if(format==31){bytes[p++]=(byte)r;bytes[p++]=(byte)g;bytes[p++]=(byte)b;}
                    else{int gray=(77*r+150*g+29*b)>>8;if(format==32)bytes[p++]=(byte)gray;else if(gray<128)bytes[x/8]|=(byte)(128>>(x%8));}
                }
            }if(format==33)p=(w+7)/8;out.write(bytes,0,p);
        }
    }
    private static void entry(OutputStream o,int tag,int type,int count,long value)throws IOException{le16(o,tag);le16(o,type);le32(o,count);le32(o,value);}
    private static void le16(OutputStream o,int v)throws IOException{o.write(v);o.write(v>>8);}
    private static void le32(OutputStream o,long v)throws IOException{for(int i=0;i<4;i++)o.write((int)(v>>(8*i)));}
    private static int u16(byte[] b,int p){return (b[p]&255)|((b[p+1]&255)<<8);}
    private static int shortAt(RandomAccessFile i,boolean le)throws IOException{int a=i.readUnsignedByte(),b=i.readUnsignedByte();return le?a|(b<<8):(a<<8)|b;}
    private static long intAt(RandomAccessFile i,boolean le)throws IOException{long a=shortAt(i,le),b=shortAt(i,le);return le?a|(b<<16):(a<<16)|b;}
    private static int read(InputStream in)throws IOException{int b=in.read();if(b<0)throw new EOFException("图片数据不完整");return b;}
    private static void fully(InputStream in,byte[] bytes)throws IOException{int p=0;while(p<bytes.length){check();int n=in.read(bytes,p,bytes.length-p);if(n<0)throw new EOFException("图片数据不完整");p+=n;}}
    private static void check()throws InterruptedIOException{if(Thread.currentThread().isInterrupted())throw new InterruptedIOException("已取消图片转换");}
}
''',
    'app/src/main/java/com/qi/formatconverter/ExtraTextFormats.java': r'''package com.qi.formatconverter;

import java.io.*;
import java.nio.charset.Charset;
import java.util.*;
import org.json.*;
import android.util.Xml;
import org.xmlpull.v1.XmlPullParser;

final class ExtraTextFormats {
    private ExtraTextFormats(){}
    static String jsonlToJson(String source)throws IOException {
        JSONArray array=new JSONArray();int line=0;
        try(BufferedReader reader=new BufferedReader(new StringReader(source))){String text;
            while((text=reader.readLine())!=null){check();line++;if(text.trim().isEmpty())continue;JSONTokener parser=new JSONTokener(text);Object value=parser.nextValue();if(parser.nextClean()!=0)throw new IOException("JSONL 第 "+line+" 行有多余内容");array.put(value);}
            return array.toString(2);
        }catch(JSONException error){throw new IOException("JSONL 第 "+line+" 行无效："+error.getMessage(),error);}
    }
    static String jsonToJsonl(String source)throws IOException {
        try{JSONTokener parser=new JSONTokener(source);Object root=parser.nextValue();if(parser.nextClean()!=0)throw new IOException("JSON 尾部有多余内容");StringBuilder text=new StringBuilder();if(root instanceof JSONArray){JSONArray array=(JSONArray)root;for(int i=0;i<array.length();i++){check();text.append(jsonValue(array.get(i))).append('\n');}}else text.append(jsonValue(root)).append('\n');return text.toString();}catch(JSONException e){throw new IOException("JSON 无效："+e.getMessage(),e);}
    }
    private static String jsonValue(Object value){String array=new JSONArray().put(value).toString();return array.substring(1,array.length()-1);}
    static String fb2Text(String source)throws IOException {
        String upper=source.toUpperCase(Locale.ROOT);if(upper.contains("<!DOCTYPE")||upper.contains("<!ENTITY"))throw new IOException("FB2 不支持 DTD 或实体");
        try{XmlPullParser parser=Xml.newPullParser();parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES,true);parser.setInput(new StringReader(source));StringBuilder text=new StringBuilder();int body=0;
            for(int event=parser.getEventType();event!=XmlPullParser.END_DOCUMENT;event=parser.next()){check();String name=parser.getName();if(event==XmlPullParser.START_TAG&&"body".equals(name))body++;else if(event==XmlPullParser.END_TAG&&"body".equals(name))body--;else if(body>0&&event==XmlPullParser.TEXT)text.append(parser.getText());else if(body>0&&event==XmlPullParser.END_TAG&&Arrays.asList("p","v","subtitle","title","empty-line").contains(name))text.append('\n');if(text.length()>DocumentKit.MAX_TEXT)throw new IOException("FB2 正文过长");}
            return text.toString().trim();
        }catch(IOException e){throw e;}catch(Exception e){throw new IOException("FB2 无法解析："+e.getMessage(),e);}
    }
    static String fb2(String text,String title){StringBuilder out=new StringBuilder("<?xml version=\"1.0\" encoding=\"UTF-8\"?><FictionBook xmlns=\"http://www.gribuser.ru/xml/fictionbook/2.0\"><description><title-info><genre>other</genre><author><nickname>未知作者</nickname></author><book-title>");out.append(DocumentKit.escape(title)).append("</book-title><lang>zh</lang></title-info><document-info><author><nickname>格式转换器</nickname></author><program-used>Format Converter</program-used><date>").append(java.time.LocalDate.now()).append("</date><id>").append(UUID.randomUUID()).append("</id><version>1.0</version></document-info></description><body><section>");for(String line:text.split("\\R",-1))out.append(line.isEmpty()?"<empty-line/>":"<p>"+DocumentKit.escape(line)+"</p>");return out.append("</section></body></FictionBook>").toString();}
    /** RTF text projection: groups, escaped bytes/code pages, Unicode fallback and ignorable destinations. */
    static String rtfText(String source)throws IOException {
        if(!source.startsWith("{\\rtf"))throw new IOException("不是有效的 RTF 文档");
        StringBuilder out=new StringBuilder();Deque<State> stack=new ArrayDeque<>();State state=new State();int skip=0;
        for(int i=0;i<source.length();){check();char c=source.charAt(i++);
            if(c=='{'){if(stack.size()>256)throw new IOException("RTF 嵌套过深");stack.push(state);state=new State(state);continue;}
            if(c=='}'){if(stack.isEmpty())throw new IOException("RTF 分组不匹配");state=stack.pop();continue;}
            if(c!='\\'){
                if(c>=128&&c<=255){ByteArrayOutputStream bytes=new ByteArrayOutputStream();bytes.write(c);while(i<source.length()&&source.charAt(i)>=128&&source.charAt(i)<=255)bytes.write(source.charAt(i++));if(!state.ignore)out.append(new String(bytes.toByteArray(),state.charset));}
                else if(c!='\r'&&c!='\n'){if(skip>0)skip--;else if(!state.ignore)out.append(c);}continue;
            }
            if(i>=source.length())break;char symbol=source.charAt(i++);
            if(symbol=='*'){state.ignore=true;continue;}
            if(symbol=='\''){
                ByteArrayOutputStream bytes=new ByteArrayOutputStream();
                while(true){if(i+2>source.length())throw new IOException("RTF 转义不完整");try{int b=Integer.parseInt(source.substring(i,i+2),16);if(skip>0)skip--;else bytes.write(b);}catch(NumberFormatException e){throw new IOException("RTF 十六进制转义无效");}i+=2;if(i+2<=source.length()&&source.charAt(i)=='\\'&&source.charAt(i+1)=='\''){i+=2;continue;}break;}
                if(!state.ignore)out.append(new String(bytes.toByteArray(),state.charset));continue;
            }
            if(!Character.isLetter(symbol)){if(skip>0)skip--;else if(!state.ignore){if(symbol=='\\'||symbol=='{'||symbol=='}')out.append(symbol);else if(symbol=='~')out.append('\u00a0');else if(symbol=='_')out.append('\u2011');}continue;}
            int begin=i-1;while(i<source.length()&&Character.isLetter(source.charAt(i)))i++;String word=source.substring(begin,i);int sign=1;if(i<source.length()&&source.charAt(i)=='-'){sign=-1;i++;}int numStart=i;while(i<source.length()&&Character.isDigit(source.charAt(i)))i++;int number=0;if(i>numStart){try{number=Math.multiplyExact(sign,Integer.parseInt(source.substring(numStart,i)));}catch(Exception e){throw new IOException("RTF 数值无效");}}if(i<source.length()&&source.charAt(i)==' ')i++;
            if(word.equals("bin")){if(number<0||number>source.length()-i)throw new IOException("RTF 二进制长度无效");i+=number;continue;}
            if(Arrays.asList("fonttbl","colortbl","stylesheet","info","pict","object","header","footer","headerl","headerr","footerl","footerr","fldinst","datastore","xmlnstbl","themedata").contains(word)){state.ignore=true;continue;}
            if(word.equals("uc")){state.uc=Math.max(0,Math.min(16,number));continue;}
            if(word.equals("ansicpg")){try{state.charset=Charset.forName(number==65001?"UTF-8":"windows-"+number);}catch(Exception e){try{state.charset=Charset.forName("CP"+number);}catch(Exception ignored){throw new IOException("RTF 字符编码不支持："+number);}}continue;}
            if(state.ignore)continue;
            if(word.equals("u")){out.append((char)number);skip=state.uc;}
            else if(word.equals("par")||word.equals("line")||word.equals("row"))out.append('\n');
            else if(word.equals("tab")||word.equals("cell"))out.append('\t');
            else if(word.equals("emdash"))out.append('—');else if(word.equals("endash"))out.append('–');else if(word.equals("bullet"))out.append('•');
            if(out.length()>DocumentKit.MAX_TEXT)throw new IOException("RTF 正文过长");
        }
        if(!stack.isEmpty())throw new IOException("RTF 分组未结束");return out.toString().trim();
    }
    private static final class State{boolean ignore;int uc=1;Charset charset=Charset.forName("windows-1252");State(){}State(State s){ignore=s.ignore;uc=s.uc;charset=s.charset;}}
    private static void check()throws InterruptedIOException{if(Thread.currentThread().isInterrupted())throw new InterruptedIOException("已取消文本转换");}
}
''',
    'app/src/main/java/com/qi/formatconverter/FastGifEncoder.java': r'''package com.qi.formatconverter;

import java.io.IOException;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.util.Arrays;

/**
 * Small streaming GIF89a encoder designed for video frames on Android.
 *
 * <p>The former encoder built millions of short-lived color objects and ran median-cut plus
 * Floyd-Steinberg dithering independently for every frame. That makes HD video several orders of
 * magnitude more expensive than decoding it. This encoder uses a perceptually balanced 6x8x5
 * color cube plus a dedicated 16-step neutral ramp, filling all 256 global palette entries,
 * a precomputed ordered-dither lookup, and a compact LZW writer. Work is linear in the number of
 * pixels, has no per-pixel allocation, and checks cancellation throughout both mapping and LZW.
 * The palette gives red/green more levels than blue, matching human visual sensitivity, while an
 * 8x8 ordered dither makes gradients finer without the large cost of per-frame color clustering.
 */
final class FastGifEncoder implements AutoCloseable {
    interface CancelCheck {
        boolean isCancelled();
    }

    private static final int PALETTE_SIZE = 256;
    private static final int RED_LEVELS = 6;
    private static final int GREEN_LEVELS = 8;
    private static final int BLUE_LEVELS = 5;
    private static final int COLOR_PALETTE_SIZE = RED_LEVELS * GREEN_LEVELS * BLUE_LEVELS;
    private static final int GRAY_LEVELS = PALETTE_SIZE - COLOR_PALETTE_SIZE;
    private static final int NEUTRAL_CHROMA_THRESHOLD = 20;
    private static final double DITHER_STRENGTH = 0.72;
    private static final int DITHER_SIZE = 8;
    private static final int[] BAYER_8X8 = {
            0, 32, 8, 40, 2, 34, 10, 42,
            48, 16, 56, 24, 50, 18, 58, 26,
            12, 44, 4, 36, 14, 46, 6, 38,
            60, 28, 52, 20, 62, 30, 54, 22,
            3, 35, 11, 43, 1, 33, 9, 41,
            51, 19, 59, 27, 49, 17, 57, 25,
            15, 47, 7, 39, 13, 45, 5, 37,
            63, 31, 55, 23, 61, 29, 53, 21
    };
    private static final byte[] GLOBAL_PALETTE = createPalette();
    private static final int[] GLOBAL_PALETTE_RGB = createPaletteRgb();
    private static final byte[][] RED_LUT = createChannelLut(RED_LEVELS);
    private static final byte[][] GREEN_LUT = createChannelLut(GREEN_LEVELS);
    private static final byte[][] BLUE_LUT = createChannelLut(BLUE_LEVELS);
    private static final byte[][] GRAY_LUT = createChannelLut(GRAY_LEVELS);

    private final OutputStream output;
    private final int width;
    private final int height;
    private final int pixelCount;
    private final CancelCheck cancelCheck;
    private final LzwWriter lzwWriter;
    private boolean finished;
    private boolean closed;

    /** loopCount follows the GIF convention: 0 means repeat forever; -1 omits the extension and plays once. */
    FastGifEncoder(
            OutputStream output,
            int width,
            int height,
            int loopCount,
            CancelCheck cancelCheck) throws IOException {
        if (output == null) throw new NullPointerException("output == null");
        if (width <= 0 || height <= 0 || width > 65535 || height > 65535) {
            throw new IllegalArgumentException("GIF 尺寸必须在 1～65535 之间");
        }
        long count = (long) width * height;
        if (count > Integer.MAX_VALUE) throw new IllegalArgumentException("GIF 尺寸过大");
        this.output = output;
        this.width = width;
        this.height = height;
        this.pixelCount = (int) count;
        this.cancelCheck = cancelCheck;
        this.lzwWriter = new LzwWriter(output, cancelCheck);
        writeHeader(Math.max(-1, Math.min(65535, loopCount)));
    }

    int pixelCount() {
        return pixelCount;
    }

    /** Converts ARGB pixels to this encoder's global palette without allocating. */
    void indexPixels(int[] argb, byte[] indexed) throws IOException {
        ensureOpen();
        if (argb == null || argb.length < pixelCount) {
            throw new IllegalArgumentException("ARGB 像素缓冲区尺寸不足");
        }
        if (indexed == null || indexed.length < pixelCount) {
            throw new IllegalArgumentException("GIF 索引缓冲区尺寸不足");
        }

        int offset = 0;
        for (int y = 0; y < height; y++) {
            if ((y & 7) == 0) checkCancelled();
            int ditherRow = (y & 7) << 3;
            for (int x = 0; x < width; x++, offset++) {
                int color = argb[offset];
                int dither = BAYER_8X8[ditherRow | (x & 7)];
                int redValue = (color >>> 16) & 0xFF;
                int greenValue = (color >>> 8) & 0xFF;
                int blueValue = color & 0xFF;
                int maximum = Math.max(redValue, Math.max(greenValue, blueValue));
                int minimum = Math.min(redValue, Math.min(greenValue, blueValue));
                if (maximum - minimum <= NEUTRAL_CHROMA_THRESHOLD) {
                    int luma = (77 * redValue + 150 * greenValue + 29 * blueValue) >>> 8;
                    indexed[offset] = (byte) (COLOR_PALETTE_SIZE
                            + (GRAY_LUT[dither][luma] & 0xFF));
                } else {
                    int red = RED_LUT[dither][redValue] & 0xFF;
                    int green = GREEN_LUT[dither][greenValue] & 0xFF;
                    int blue = BLUE_LUT[dither][blueValue] & 0xFF;
                    indexed[offset] = (byte) ((red * GREEN_LEVELS + green)
                            * BLUE_LEVELS + blue);
                }
            }
        }
    }

    static int paletteRgb(int paletteIndex) {
        return GLOBAL_PALETTE_RGB[paletteIndex & 0xFF];
    }

    void addFrame(int[] argb, byte[] indexedScratch, int delayMs) throws IOException {
        indexPixels(argb, indexedScratch);
        addIndexedFrame(indexedScratch, delayMs);
    }

    void addIndexedFrame(byte[] indexed, int delayMs) throws IOException {
        ensureOpen();
        if (indexed == null || indexed.length < pixelCount) {
            throw new IllegalArgumentException("GIF 索引帧尺寸不足");
        }
        checkCancelled();
        writeGraphicControlExtension(delayMs);
        writeImageDescriptor();
        lzwWriter.write(indexed, pixelCount);
        checkCancelled();
    }

    void finish() throws IOException {
        if (finished) return;
        ensureOpen();
        checkCancelled();
        output.write(0x3B);
        output.flush();
        finished = true;
    }

    private void writeHeader(int loopCount) throws IOException {
        writeAscii("GIF89a");
        writeLittleEndian(width);
        writeLittleEndian(height);
        // Global color table, 8-bit color resolution, 256 entries.
        output.write(0xF7);
        output.write(0);
        output.write(0);
        output.write(GLOBAL_PALETTE);

        if (loopCount < 0) return; // No looping extension: play once.
        output.write(0x21);
        output.write(0xFF);
        output.write(11);
        writeAscii("NETSCAPE2.0");
        output.write(3);
        output.write(1);
        writeLittleEndian(loopCount);
        output.write(0);
    }

    private void writeGraphicControlExtension(int delayMs) throws IOException {
        int delayCentiseconds = Math.max(1, Math.min(65535, (delayMs + 5) / 10));
        output.write(0x21);
        output.write(0xF9);
        output.write(4);
        // Disposal method 1: retain the completed frame; no transparency.
        output.write(0x04);
        writeLittleEndian(delayCentiseconds);
        output.write(0);
        output.write(0);
    }

    private void writeImageDescriptor() throws IOException {
        output.write(0x2C);
        writeLittleEndian(0);
        writeLittleEndian(0);
        writeLittleEndian(width);
        writeLittleEndian(height);
        output.write(0);
    }

    private void writeAscii(String value) throws IOException {
        for (int i = 0; i < value.length(); i++) output.write(value.charAt(i));
    }

    private void writeLittleEndian(int value) throws IOException {
        output.write(value & 0xFF);
        output.write((value >>> 8) & 0xFF);
    }

    private void ensureOpen() {
        if (closed) throw new IllegalStateException("GIF 编码器已经关闭");
        if (finished) throw new IllegalStateException("GIF 编码已经结束");
    }

    private void checkCancelled() throws InterruptedIOException {
        if (Thread.currentThread().isInterrupted()
                || (cancelCheck != null && cancelCheck.isCancelled())) {
            throw new InterruptedIOException("转换已取消");
        }
    }

    @Override public void close() throws IOException {
        if (closed) return;
        closed = true;
        // The caller owns the stream. A failed/cancelled partial GIF is intentionally not finalized.
        output.flush();
    }

    private static byte[] createPalette() {
        byte[] palette = new byte[PALETTE_SIZE * 3];
        int index = 0;
        for (int red = 0; red < RED_LEVELS; red++) {
            for (int green = 0; green < GREEN_LEVELS; green++) {
                for (int blue = 0; blue < BLUE_LEVELS; blue++) {
                    int base = index++ * 3;
                    palette[base] = (byte) Math.round(red * 255f / (RED_LEVELS - 1));
                    palette[base + 1] = (byte) Math.round(green * 255f / (GREEN_LEVELS - 1));
                    palette[base + 2] = (byte) Math.round(blue * 255f / (BLUE_LEVELS - 1));
                }
            }
        }
        for (int gray = 0; gray < GRAY_LEVELS; gray++) {
            int value = Math.round(gray * 255f / (GRAY_LEVELS - 1));
            int base = index++ * 3;
            palette[base] = (byte) value;
            palette[base + 1] = (byte) value;
            palette[base + 2] = (byte) value;
        }
        return palette;
    }

    private static byte[][] createChannelLut(int levels) {
        byte[][] lut = new byte[DITHER_SIZE * DITHER_SIZE][256];
        double step = 255.0 / (levels - 1);
        for (int dither = 0; dither < DITHER_SIZE * DITHER_SIZE; dither++) {
            double adjustment = ((dither + 0.5) / (DITHER_SIZE * DITHER_SIZE)
                    - 0.5) * step * DITHER_STRENGTH;
            for (int value = 0; value < 256; value++) {
                int adjusted = (int) Math.round(value + adjustment);
                adjusted = Math.max(0, Math.min(255, adjusted));
                lut[dither][value] = (byte) Math.max(0, Math.min(levels - 1,
                        (adjusted * (levels - 1) + 127) / 255));
            }
        }
        return lut;
    }

    private static int[] createPaletteRgb() {
        int[] colors = new int[PALETTE_SIZE];
        for (int index = 0; index < colors.length; index++) {
            int base = index * 3;
            colors[index] = ((GLOBAL_PALETTE[base] & 0xFF) << 16)
                    | ((GLOBAL_PALETTE[base + 1] & 0xFF) << 8)
                    | (GLOBAL_PALETTE[base + 2] & 0xFF);
        }
        return colors;
    }

    /** GIF LZW with an allocation-free open-addressed dictionary and 255-byte sub-blocks. */
    private static final class LzwWriter {
        private static final int MIN_CODE_SIZE = 8;
        private static final int CLEAR_CODE = 1 << MIN_CODE_SIZE;
        private static final int END_CODE = CLEAR_CODE + 1;
        private static final int FIRST_CODE = END_CODE + 1;
        private static final int MAX_CODE = 4095;
        private static final int HASH_SIZE = 8192;
        private static final int HASH_MASK = HASH_SIZE - 1;

        private final OutputStream output;
        private final CancelCheck cancelCheck;
        private final int[] keys = new int[HASH_SIZE];
        private final short[] values = new short[HASH_SIZE];
        private final byte[] block = new byte[255];
        private int blockLength;
        private int bitBuffer;
        private int bitCount;
        private int codeSize;
        private int nextCode;
        private int codeLimit;

        LzwWriter(OutputStream output, CancelCheck cancelCheck) {
            this.output = output;
            this.cancelCheck = cancelCheck;
        }

        void write(byte[] pixels, int length) throws IOException {
            output.write(MIN_CODE_SIZE);
            blockLength = 0;
            bitBuffer = 0;
            bitCount = 0;
            resetDictionary();
            writeCode(CLEAR_CODE);

            int prefix = pixels[0] & 0xFF;
            for (int i = 1; i < length; i++) {
                if ((i & 0x3FFF) == 0) checkCancelled();
                int suffix = pixels[i] & 0xFF;
                int key = (prefix << 8) | suffix;
                int slot = findSlot(key);
                if (keys[slot] != 0) {
                    prefix = values[slot] & 0xFFFF;
                    continue;
                }

                writeCode(prefix);
                if (nextCode <= MAX_CODE) {
                    keys[slot] = key + 1;
                    values[slot] = (short) nextCode++;
                    // Grow only after the first code that needs the wider size has been added.
                    // GIF decoders add the same dictionary entry one code later than encoders;
                    // advancing at equality makes the stream one bit early and corrupts HD frames.
                    if (nextCode > codeLimit && codeSize < 12) {
                        codeSize++;
                        codeLimit <<= 1;
                    }
                } else {
                    writeCode(CLEAR_CODE);
                    resetDictionary();
                }
                prefix = suffix;
            }

            writeCode(prefix);
            writeCode(END_CODE);
            flushBits();
            flushBlock();
            output.write(0);
        }

        private int findSlot(int key) {
            int slot = (key * 0x9E3779B9) & HASH_MASK;
            int storedKey = key + 1;
            while (keys[slot] != 0 && keys[slot] != storedKey) {
                slot = (slot + 1) & HASH_MASK;
            }
            return slot;
        }

        private void resetDictionary() {
            Arrays.fill(keys, 0);
            codeSize = MIN_CODE_SIZE + 1;
            nextCode = FIRST_CODE;
            codeLimit = 1 << codeSize;
        }

        private void writeCode(int code) throws IOException {
            bitBuffer |= code << bitCount;
            bitCount += codeSize;
            while (bitCount >= 8) {
                writeByte(bitBuffer & 0xFF);
                bitBuffer >>>= 8;
                bitCount -= 8;
            }
        }

        private void flushBits() throws IOException {
            if (bitCount > 0) {
                writeByte(bitBuffer & 0xFF);
                bitBuffer = 0;
                bitCount = 0;
            }
        }

        private void writeByte(int value) throws IOException {
            block[blockLength++] = (byte) value;
            if (blockLength == block.length) flushBlock();
        }

        private void flushBlock() throws IOException {
            if (blockLength == 0) return;
            output.write(blockLength);
            output.write(block, 0, blockLength);
            blockLength = 0;
        }

        private void checkCancelled() throws InterruptedIOException {
            if (Thread.currentThread().isInterrupted()
                    || (cancelCheck != null && cancelCheck.isCancelled())) {
                throw new InterruptedIOException("转换已取消");
            }
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/FrameEditor.java': r'''package com.qi.formatconverter;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.ColorMatrix;
import android.graphics.ColorMatrixColorFilter;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;

/** Reusable, GPU-friendly canvas transform for the lightweight animation editor. */
final class FrameEditor {
    private static final ThreadLocal<DrawScratch> DRAW_SCRATCH =
            ThreadLocal.withInitial(DrawScratch::new);

    private FrameEditor() { }

    static int[] editedSize(int sourceWidth, int sourceHeight, AnimationEdits edits) {
        int width = Math.max(1, sourceWidth);
        int height = Math.max(1, sourceHeight);
        double aspect = edits.cropAspect();
        if (aspect > 0.0) {
            if (width / (double) height > aspect) {
                width = Math.max(1, (int) Math.round(height * aspect));
            } else {
                height = Math.max(1, (int) Math.round(width / aspect));
            }
        }
        if (edits.rotationDegrees == 90 || edits.rotationDegrees == 270) {
            int swap = width;
            width = height;
            height = swap;
        }
        return new int[]{width, height};
    }

    /**
     * Returns full-frame decoder bounds large enough that a later center crop does not discard
     * resolution. The decoder still applies its own no-upscale rule.
     */
    static int[] decodeBounds(
            int sourceWidth, int sourceHeight,
            int outputWidth, int outputHeight,
            AnimationEdits edits) {
        int sourceW = Math.max(1, sourceWidth);
        int sourceH = Math.max(1, sourceHeight);
        int preWidth = Math.max(1, outputWidth);
        int preHeight = Math.max(1, outputHeight);
        if (edits.rotationDegrees == 90 || edits.rotationDegrees == 270) {
            int swap = preWidth;
            preWidth = preHeight;
            preHeight = swap;
        }

        double cropWidth = sourceW;
        double cropHeight = sourceH;
        double aspect = edits.cropAspect();
        if (aspect > 0.0) {
            if (sourceW / (double) sourceH > aspect) cropWidth = sourceH * aspect;
            else cropHeight = sourceW / aspect;
        }
        double scale = Math.min(1.0,
                Math.max(preWidth / cropWidth, preHeight / cropHeight));
        int width = Math.max(1, Math.min(4096, (int) Math.ceil(sourceW * scale)));
        int height = Math.max(1, Math.min(4096, (int) Math.ceil(sourceH * scale)));
        return new int[]{width, height};
    }

    static Paint createPaint(AnimationEdits edits) {
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG
                | Paint.FILTER_BITMAP_FLAG | Paint.DITHER_FLAG);
        if (edits.brightness == 0
                && edits.contrast == 100
                && edits.saturation == 100) {
            return paint;
        }

        ColorMatrix saturation = new ColorMatrix();
        saturation.setSaturation(edits.saturation / 100f);
        float contrast = edits.contrast / 100f;
        float brightnessOffset = edits.brightness * 2.55f;
        float centerOffset = 128f * (1f - contrast) + brightnessOffset;
        ColorMatrix adjustment = new ColorMatrix(new float[]{
                contrast, 0, 0, 0, centerOffset,
                0, contrast, 0, 0, centerOffset,
                0, 0, contrast, 0, centerOffset,
                0, 0, 0, 1, 0
        });
        adjustment.postConcat(saturation);
        paint.setColorFilter(new ColorMatrixColorFilter(adjustment));
        return paint;
    }

    static void drawBitmap(
            Canvas target, Bitmap source, int background,
            AnimationEdits edits, Paint paint) {
        int targetWidth = target.getWidth();
        int targetHeight = target.getHeight();
        target.drawColor(background);

        float sourceWidth = source.getWidth();
        float sourceHeight = source.getHeight();
        float cropLeft = 0f;
        float cropTop = 0f;
        float cropRight = sourceWidth;
        float cropBottom = sourceHeight;
        double cropAspect = edits.cropAspect();
        if (cropAspect > 0.0) {
            if (sourceWidth / sourceHeight > cropAspect) {
                float cropWidth = (float) (sourceHeight * cropAspect);
                cropLeft = (sourceWidth - cropWidth) * 0.5f;
                cropRight = cropLeft + cropWidth;
            } else {
                float cropHeight = (float) (sourceWidth / cropAspect);
                cropTop = (sourceHeight - cropHeight) * 0.5f;
                cropBottom = cropTop + cropHeight;
            }
        }

        float preWidth = targetWidth;
        float preHeight = targetHeight;
        if (edits.rotationDegrees == 90 || edits.rotationDegrees == 270) {
            preWidth = targetHeight;
            preHeight = targetWidth;
        }
        float drawWidth = preWidth;
        float drawHeight = preHeight;
        if (cropAspect <= 0.0) {
            float scale = Math.min(
                    preWidth / Math.max(1f, cropRight - cropLeft),
                    preHeight / Math.max(1f, cropBottom - cropTop));
            drawWidth = (cropRight - cropLeft) * scale;
            drawHeight = (cropBottom - cropTop) * scale;
        }

        int save = target.save();
        target.translate(targetWidth * 0.5f, targetHeight * 0.5f);
        target.scale(edits.flipHorizontal ? -1f : 1f,
                edits.flipVertical ? -1f : 1f);
        target.rotate(edits.rotationDegrees);
        DrawScratch scratch = DRAW_SCRATCH.get();
        scratch.source.set(Math.round(cropLeft), Math.round(cropTop),
                Math.round(cropRight), Math.round(cropBottom));
        scratch.destination.set(-drawWidth * 0.5f, -drawHeight * 0.5f,
                drawWidth * 0.5f, drawHeight * 0.5f);
        target.drawBitmap(source,
                scratch.source, scratch.destination, paint);
        target.restoreToCount(save);
    }

    private static final class DrawScratch {
        final Rect source = new Rect();
        final RectF destination = new RectF();
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/IcoWriter.java': r'''package com.qi.formatconverter;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.List;

/**
 * Dependency-free writer for Windows .ico icon files using the modern
 * PNG-in-ICO layout (supported by Windows Vista and every current browser
 * and image viewer). Each frame is a complete PNG image embedded as-is.
 */
public final class IcoWriter {

    private static final byte[] PNG_SIGNATURE = {
            (byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A
    };

    /** One square icon frame: PNG bytes plus its side length in pixels. */
    public static final class Frame {
        public final byte[] png;
        public final int size;

        public Frame(byte[] png, int size) {
            if (png == null || png.length < 8) {
                throw new IllegalArgumentException("PNG data is empty");
            }
            for (int i = 0; i < PNG_SIGNATURE.length; i++) {
                if (png[i] != PNG_SIGNATURE[i]) {
                    throw new IllegalArgumentException("Frame data is not PNG");
                }
            }
            if (size <= 0 || size > 256) {
                throw new IllegalArgumentException("Illegal icon frame size");
            }
            this.png = png;
            this.size = size;
        }
    }

    private IcoWriter() { }

    /** Writes the frames (ascending size order recommended) into an .ico file. */
    public static void write(File output, List<Frame> frames) throws IOException {
        if (frames == null || frames.isEmpty()) {
            throw new IOException("没有可写入的图标帧");
        }
        if (frames.size() > 0xFFFF) {
            throw new IOException("图标帧数量过多");
        }
        long dataOffset = 6L + 16L * frames.size();
        for (Frame frame : frames) {
            dataOffset += frame.png.length;
        }
        if (dataOffset > Integer.MAX_VALUE) {
            throw new IOException("图标文件过大");
        }

        try (OutputStream out = new BufferedOutputStream(
                new FileOutputStream(output), 64 * 1024)) {
            // ICONDIR: reserved=0, type=1 (icon), frame count. Little-endian integers.
            writeShort(out, 0);
            writeShort(out, 1);
            writeShort(out, frames.size());

            long offset = 6L + 16L * frames.size();
            for (Frame frame : frames) {
                // ICONDIRENTRY: 0 means 256 pixels.
                int stored = frame.size == 256 ? 0 : frame.size;
                out.write(stored);
                out.write(stored);
                out.write(0); // palette colors, 0 = true color
                out.write(0); // reserved
                writeShort(out, 1); // color planes
                writeShort(out, 32); // bits per pixel
                writeInt(out, frame.png.length);
                writeInt(out, (int) offset);
                offset += frame.png.length;
            }
            for (Frame frame : frames) {
                out.write(frame.png, 0, frame.png.length);
            }
        }
        if (output.length() <= 0) {
            throw new IOException("ICO 生成失败");
        }
    }

    private static void writeShort(OutputStream out, int value) throws IOException {
        out.write(value & 0xFF);
        out.write((value >>> 8) & 0xFF);
    }

    private static void writeInt(OutputStream out, long value) throws IOException {
        out.write((int) (value & 0xFF));
        out.write((int) ((value >>> 8) & 0xFF));
        out.write((int) ((value >>> 16) & 0xFF));
        out.write((int) ((value >>> 24) & 0xFF));
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/IndexedFrameStore.java': r'''package com.qi.formatconverter;

import java.io.File;
import java.io.IOException;
import java.io.InterruptedIOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.DataFormatException;
import java.util.zip.Deflater;
import java.util.zip.Inflater;

/**
 * Compact seekable cache for palette-indexed frames used by reverse and repeated playback.
 *
 * <p>Frames are compressed directly as palette indexes. This avoids the old JPEG encode -> disk
 * -> JPEG decode round trip, keeps reverse playback lossless, and normally uses substantially less
 * cache than raw ARGB bitmaps.
 */
final class IndexedFrameStore implements AutoCloseable {
    interface CancelCheck {
        boolean isCancelled();
    }

    private final File backingFile;
    private final RandomAccessFile file;
    private final int frameSize;
    private final CancelCheck cancelCheck;
    private final List<Long> offsets = new ArrayList<>();
    private final Deflater deflater = new Deflater(Deflater.BEST_SPEED, true);
    private final Inflater inflater = new Inflater(true);
    private byte[] compressedWrite;
    private byte[] compressedRead = new byte[0];
    private boolean closed;

    IndexedFrameStore(File backingFile, int frameSize, CancelCheck cancelCheck) throws IOException {
        if (frameSize <= 0) throw new IllegalArgumentException("frameSize <= 0");
        this.backingFile = backingFile;
        this.frameSize = frameSize;
        this.cancelCheck = cancelCheck;
        int overhead = Math.max(128, frameSize / 100 + 64);
        compressedWrite = new byte[frameSize + overhead];
        file = new RandomAccessFile(backingFile, "rw");
        file.setLength(0);
    }

    int size() {
        return offsets.size();
    }

    long compressedBytes() throws IOException {
        ensureOpen();
        return file.length();
    }

    void add(byte[] indexedFrame) throws IOException {
        ensureOpen();
        checkCancelled();
        if (indexedFrame == null || indexedFrame.length < frameSize) {
            throw new IllegalArgumentException("索引帧尺寸不足");
        }

        deflater.reset();
        deflater.setInput(indexedFrame, 0, frameSize);
        deflater.finish();
        int length = 0;
        while (!deflater.finished()) {
            if (length == compressedWrite.length) growWriteBuffer();
            int count = deflater.deflate(
                    compressedWrite, length, compressedWrite.length - length);
            if (count <= 0 && !deflater.finished()) {
                growWriteBuffer();
            } else {
                length += count;
            }
            checkCancelled();
        }

        offsets.add(file.getFilePointer());
        file.writeInt(length);
        file.write(compressedWrite, 0, length);
    }

    void read(int frameIndex, byte[] destination) throws IOException {
        ensureOpen();
        checkCancelled();
        if (frameIndex < 0 || frameIndex >= offsets.size()) {
            throw new IndexOutOfBoundsException("frameIndex=" + frameIndex);
        }
        if (destination == null || destination.length < frameSize) {
            throw new IllegalArgumentException("目标索引帧尺寸不足");
        }

        file.seek(offsets.get(frameIndex));
        int compressedLength = file.readInt();
        if (compressedLength <= 0 || compressedLength > frameSize + frameSize / 2 + 4096) {
            throw new IOException("倒放帧缓存已损坏");
        }
        if (compressedRead.length < compressedLength) {
            compressedRead = new byte[compressedLength];
        }
        file.readFully(compressedRead, 0, compressedLength);

        inflater.reset();
        inflater.setInput(compressedRead, 0, compressedLength);
        int written = 0;
        try {
            while (written < frameSize && !inflater.finished()) {
                int count = inflater.inflate(destination, written, frameSize - written);
                if (count == 0) {
                    if (inflater.needsInput() || inflater.needsDictionary()) break;
                    throw new IOException("倒放帧缓存无法继续解压");
                }
                written += count;
                checkCancelled();
            }
        } catch (DataFormatException error) {
            throw new IOException("倒放帧缓存已损坏", error);
        }
        if (written != frameSize || !inflater.finished()) {
            throw new IOException("倒放帧缓存长度不正确");
        }
        checkCancelled();
    }

    private void growWriteBuffer() {
        int oldLength = compressedWrite.length;
        compressedWrite = java.util.Arrays.copyOf(
                compressedWrite, oldLength + Math.max(4096, oldLength / 4));
    }

    private void ensureOpen() throws IOException {
        if (closed) throw new IOException("帧缓存已经关闭");
    }

    private void checkCancelled() throws InterruptedIOException {
        if (Thread.currentThread().isInterrupted()
                || (cancelCheck != null && cancelCheck.isCancelled())) {
            throw new InterruptedIOException("转换已取消");
        }
    }

    @Override public void close() {
        if (closed) return;
        closed = true;
        deflater.end();
        inflater.end();
        try { file.close(); } catch (Exception ignored) { }
        try { backingFile.delete(); } catch (Exception ignored) { }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/MainActivity.java': r'''package com.qi.formatconverter;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ClipData;
import android.content.ComponentCallbacks2;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ImageDecoder;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.media.MediaMetadataRetriever;
import android.graphics.pdf.PdfRenderer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.ParcelFileDescriptor;
import android.provider.DocumentsContract;
import android.provider.OpenableColumns;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.util.Log;
import android.util.LruCache;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.PopupMenu;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Locale;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.Executors;
import java.util.zip.Deflater;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import pl.droidsonroids.gif.GifDrawable;
import pl.droidsonroids.gif.LibraryLoader;

public class MainActivity extends Activity {
    private static final int REQUEST_PICK = 1001;
    private static final int REQUEST_MUSIC = 1004;
    private static final int REQUEST_SAVE = 1002;
    private static final int REQUEST_SAVE_FOLDER = 1003;
    private static final int ZIP_SUGGEST_THRESHOLD = 20;
    private static final String EDITOR_PREFS = "editor_preferences";
    private static final String PREF_EDITOR_BRIGHTNESS = "brightness";
    private static final String PREF_EDITOR_CONTRAST = "contrast";
    private static final String PREF_EDITOR_SATURATION = "saturation";
    private static final int DEFAULT_EDITOR_BRIGHTNESS = 0;
    private static final int DEFAULT_EDITOR_CONTRAST = 90;
    private static final int DEFAULT_EDITOR_SATURATION = 100;

    private static final String[] OUTPUT_FORMATS = {
            "JPEG",
            "PNG",
            "BMP",
            "GIF",
            "MP4（H.264/AVC，兼容优先）",
            "MP4（H.265/HEVC，省空间）",
            "MP4（AV1，新设备高压缩）",
            "WebP（有损）",
            "WebP（无损）",
            "MP3（音频转换 / 视频提取）",
            "M4A（AAC 原样提取 / 兼容转码）",
            "PDF（图片合成 / 多个 PDF 合并）",
            "ICO 图标（Windows 多尺寸图标）",
            "TXT 纯文本（含 PDF / DOCX / EPUB / ODT）",
            "HTML 网页（Markdown/CSV/TSV/JSON）",
            "CSV 表格（JSON/MD/TSV/YAML）",
            "JSON（CSV/MD/TSV/YAML/XML/字幕）",
            "YAML（JSON/CSV/TSV/MD 表格）",
            "XML（JSON/YAML/CSV/TSV/MD 表格）",
            "Markdown（表格 / 文档正文）",
            "TSV（CSV/MD/JSON/YAML 表格）",
            "VTT 字幕（SRT 转 WebVTT）",
            "SRT 字幕（VTT 转 SubRip）",
            "PDF 文档（可选中文字 / A4 排版）",
            "DOCX 文档（正文转换）",
            "EPUB 电子书（正文转换）",
            "ODT 文档（正文转换）",
            "WAV 音频（48 kHz / 16 bit / 双声道）",
            "RTF 文档（富文本兼容导出）",
            "TIFF（无损 RGBA / 未压缩）",
            "TGA（32 bit / 保留透明）",
            "PPM（RGB 无损 / 无透明）",
            "PGM（8 bit 灰度）",
            "PBM（黑白二值）",
            "PAM（RGBA 无损 / 保留透明）",
            "JSONL / NDJSON（每行一条 JSON）",
            "FB2 电子书（正文转换）"
    };
    private static final String[] RESOLUTION_OPTIONS = {
            "智能推荐（按画质、尺寸与时长）",
            "保持原始",
            "640×480 以内",
            "1280×720 以内",
            "1920×1080 以内",
            "2560×1440 以内",
            "3840×2160 以内",
            "自定义"
    };
    private static final String[] FPS_OPTIONS = {
            "5 FPS", "10 FPS", "12 FPS", "15 FPS", "20 FPS",
            "24 FPS", "30 FPS", "60 FPS", "自定义"
    };
    private static final String[] FRAME_LIMIT_OPTIONS = {
            "300 帧", "600 帧", "1000 帧", "2000 帧", "5000 帧", "自定义"
    };
    private static final String[] BITRATE_OPTIONS = {
            "自动", "2 Mbps", "4 Mbps", "8 Mbps", "12 Mbps",
            "20 Mbps", "40 Mbps", "自定义"
    };
    private static final String[] LOOP_OPTIONS = {
            "1 次", "2 次", "3 次", "5 次", "10 次", "自定义"
    };
    private static final String[] REVERSE_LOOP_OPTIONS = {
            "不倒放", "第 1 次倒放", "第 2 次倒放", "第 3 次倒放", "第 5 次倒放", "第 10 次倒放", "自定义轮次", "每次都倒放", "往返播放（正放 → 倒放）"
    };
    private static final String[] VIDEO_GIF_OUTPUT_OPTIONS = {
            "合并为 1 个 GIF（默认）",
            "批量生成（每个视频 1 个 GIF）"
    };
    private static final String[] EDIT_SPEED_OPTIONS = {
            "0.25×", "0.5×", "0.75×", "1×", "1.25×", "1.5×", "2×", "3×", "4×"
    };
    private static final double[] EDIT_SPEED_VALUES = {
            0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0
    };
    private static final String[] EDIT_CROP_OPTIONS = {
            "不裁切", "1:1", "4:3", "3:4", "16:9", "9:16"
    };
    private static final String[] EDIT_ROTATION_OPTIONS = {
            "不旋转", "顺时针 90°", "旋转 180°", "顺时针 270°"
    };

    private static final int PRIMARY = 0xFF5757D9;
    private static final int DISABLED = 0xFFB7B9C5;
    private static final int PRIMARY_TEXT = 0xFF20212A;
    private static final int SECONDARY_TEXT = 0xFF686A75;

    private final List<SelectedItem> selectedItems = new ArrayList<>();
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final ExecutorService thumbnailExecutor = new java.util.concurrent.ThreadPoolExecutor(
            2, 2, 0L, java.util.concurrent.TimeUnit.MILLISECONDS,
            new java.util.concurrent.ArrayBlockingQueue<>(32),
            new java.util.concurrent.ThreadPoolExecutor.DiscardOldestPolicy());
    private final LruCache<String, Bitmap> thumbnailCache =
            new LruCache<String, Bitmap>(thumbnailCacheKilobytes()) {
        @Override protected int sizeOf(String key, Bitmap bitmap) {
            return Math.max(1, bitmap.getAllocationByteCount() / 1024);
        }
    };

    private TextView selectionSummary;
    private TextView qualityText;
    private AlertDialog activeEditorDialog;
    private AlertDialog activeAudioDialog;
    private Runnable pauseEditorPreview;
    private Runnable refreshEditorAudio;

    private TextView recommendationText;
    private Uri backgroundMusic;
    private float originalVolume = 1f, musicVolume = 0.5f;
    private boolean musicLoop = true;
    private double musicStartSeconds = 0, audioFadeSeconds = 0;
    private AudioPipeline.Settings exportAudioSettings;
    private final Handler recommendationHandler = new Handler(Looper.getMainLooper());
    private final ExecutorService recommendationExecutor = Executors.newSingleThreadExecutor();
    private Future<?> recommendationTask;
    private int recommendationGeneration;
    private TextView statusText;
    private TextView progressText;
    private TextView codecSupportText;
    private RecyclerView selectedRecycler;
    private SelectedFileAdapter selectedAdapter;
    private ItemTouchHelper itemTouchHelper;
    private Spinner formatSpinner;
    private final List<Integer> visibleOutputFormats = new ArrayList<>();
    private boolean refreshingOutputFormats;
    private Spinner resolutionSpinner;
    private Spinner fpsSpinner;
    private Spinner frameLimitSpinner;
    private Spinner bitrateSpinner;
    private Spinner loopSpinner;
    private Spinner videoLoopSpinner;
    private Spinner reverseLoopSpinner;
    private Spinner gifReplaySpinner;
    private View gifReplayLabel;
    private Spinner videoGifOutputSpinner;
    private SeekBar qualitySeek;
    private View resolutionLabel;
    private View resolutionCustomRow;
    private View fpsLabel;
    private View frameLimitLabel;
    private View bitrateLabel;
    private View loopLabel;
    private View videoGifOutputLabel;
    private View videoLoopLabel;
    private View reverseLoopLabel;
    private View animationOptionsHint;
    private EditText customWidthEdit;
    private EditText customHeightEdit;
    private EditText customFpsEdit;
    private EditText customFrameLimitEdit;
    private EditText customBitrateEdit;
    private EditText customLoopEdit;
    private EditText customVideoLoopEdit;
    private EditText customReverseLoopEdit;
    private Button addButton;
    private Button clearButton;
    private Button editButton;
    private Button convertButton;
    private Button cancelButton;
    private ProgressBar progressBar;

    private volatile boolean cancelRequested;
    private volatile boolean taskRunning;
    private volatile boolean busy;
    private volatile Future<?> currentTask;
    private volatile File activeWorkFile;
    private volatile ConversionSettings runningSettings;
    private volatile long lastProgressPostNanos;
    private volatile int lastProgressPostValue = -1;
    private volatile int progressMapStart;
    private volatile int progressMapSpan = 1000;
    private volatile String progressMapPrefix = "";
    private boolean qualityTouched;
    private boolean h264Supported;
    private boolean h265Supported;
    private boolean av1Supported;
    private AnimationEdits animationEdits;
    private File pendingOutput;
    private String pendingFileName;
    private List<PendingBatchFile> pendingBatchFiles;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        LibraryLoader.initialize(this);
        cleanupStaleConversionFiles();
        animationEdits = freshAnimationEdits();
        buildUi();
        handleIncomingShareIntent(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleIncomingShareIntent(intent);
    }

    private void buildUi() {
        int bg = 0xFFF6F7FB;
        int card = 0xFFFFFFFF;

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setFitsSystemWindows(true);
        scroll.setBackgroundColor(bg);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(18), dp(22), dp(18), dp(32));
        scroll.addView(root, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView title = text("格式转换器", 28, PRIMARY_TEXT, true);
        title.setPadding(0, 0, 0, dp(16));
        root.addView(title);
        // Keep the landing page compact: the title is enough.

        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setPadding(dp(15), dp(15), dp(15), dp(17));
        panel.setBackground(roundRect(card, 18));
        root.addView(panel, matchWrap());

        LinearLayout fileButtons = horizontalRow();
        fileButtons.setPadding(0, 0, 0, 0);
        addButton = createButton("添加文件", true);
        clearButton = createButton("清空", false);
        addTwoButtons(fileButtons, addButton, clearButton);
        panel.addView(fileButtons, matchWrap());
        addButton.setOnClickListener(v -> openFilePicker());
        clearButton.setOnClickListener(v -> confirmClearSelection());

        selectionSummary = text("尚未选择文件", 14, SECONDARY_TEXT, false);
        selectionSummary.setPadding(0, dp(10), 0, dp(8));
        panel.addView(selectionSummary);

        selectedRecycler = new RecyclerView(this);
        selectedRecycler.setLayoutManager(new LinearLayoutManager(this));
        selectedRecycler.setNestedScrollingEnabled(false);
        selectedRecycler.setItemAnimator(null);
        selectedAdapter = new SelectedFileAdapter();
        selectedRecycler.setAdapter(selectedAdapter);
        selectedRecycler.setVisibility(View.GONE);
        panel.addView(selectedRecycler, matchWrap());

        ItemTouchHelper.SimpleCallback dragCallback = new ItemTouchHelper.SimpleCallback(
                ItemTouchHelper.UP | ItemTouchHelper.DOWN, 0) {
            @Override public boolean onMove(
                    RecyclerView recyclerView,
                    RecyclerView.ViewHolder source,
                    RecyclerView.ViewHolder target) {
                if (busy) return false;
                int from = source.getBindingAdapterPosition();
                int to = target.getBindingAdapterPosition();
                if (from == RecyclerView.NO_POSITION || to == RecyclerView.NO_POSITION) return false;
                Collections.swap(selectedItems, from, to);
                animationEdits = freshAnimationEdits();
                selectedAdapter.notifyItemMoved(from, to);
                int start = Math.min(from, to);
                selectedAdapter.notifyItemRangeChanged(start, Math.abs(from - to) + 1);
                updateSelectionUi();
                return true;
            }
            @Override public void onSwiped(RecyclerView.ViewHolder viewHolder, int direction) { }
            @Override public boolean isLongPressDragEnabled() { return false; }
            @Override public boolean isItemViewSwipeEnabled() { return false; }
            @Override public void clearView(RecyclerView recyclerView, RecyclerView.ViewHolder viewHolder) {
                super.clearView(recyclerView, viewHolder);
                selectedAdapter.notifyDataSetChanged();
                updateSelectionUi();
            }
        };
        itemTouchHelper = new ItemTouchHelper(dragCallback);
        itemTouchHelper.attachToRecyclerView(selectedRecycler);

        // Reordering remains available by long-press; no persistent helper copy is needed.

        addLabel(panel, "输出格式", PRIMARY_TEXT);
        visibleOutputFormats.clear();
        for (int i = 0; i < OUTPUT_FORMATS.length; i++) visibleOutputFormats.add(i);
        formatSpinner = createSpinner(OUTPUT_FORMATS);
        panel.addView(formatSpinner, matchWrap());

        qualityText = text("图片质量：92", 15, PRIMARY_TEXT, false);
        qualityText.setPadding(0, dp(17), 0, 0);
        panel.addView(qualityText);
        qualitySeek = new SeekBar(this);
        qualitySeek.setMin(1);
        qualitySeek.setMax(100);
        qualitySeek.setProgress(92);
        qualitySeek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (fromUser) qualityTouched = true;
                updateControlStates();
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) { }
            @Override public void onStopTrackingTouch(SeekBar seekBar) { }
        });
        panel.addView(qualitySeek, matchWrap());

        resolutionLabel = addLabelWithTop(panel, "输出分辨率", PRIMARY_TEXT);
        resolutionSpinner = createSpinner(RESOLUTION_OPTIONS);
        resolutionSpinner.setSelection(0);
        panel.addView(resolutionSpinner, matchWrap());
        recommendationText = text("添加文件后显示推荐尺寸", 13, SECONDARY_TEXT, false);
        recommendationText.setPadding(dp(4), dp(8), dp(4), dp(10));
        recommendationText.setTextIsSelectable(true);
        panel.addView(recommendationText, matchWrap());

        LinearLayout resolutionRow = horizontalRow();
        customWidthEdit = numberField("自定义宽度", "1280", false);
        customHeightEdit = numberField("自定义高度", "720", false);
        addTwoFields(resolutionRow, customWidthEdit, customHeightEdit);
        panel.addView(resolutionRow, matchWrap());
        resolutionCustomRow = resolutionRow;

        fpsLabel = addLabelWithTop(panel, "帧率", PRIMARY_TEXT);
        fpsSpinner = createSpinner(FPS_OPTIONS);
        fpsSpinner.setSelection(2);
        panel.addView(fpsSpinner, matchWrap());
        customFpsEdit = numberField("自定义 FPS（1–120）", "12", true);
        panel.addView(customFpsEdit, fieldParams());

        frameLimitLabel = addLabelWithTop(panel, "最大处理帧数", PRIMARY_TEXT);
        frameLimitSpinner = createSpinner(FRAME_LIMIT_OPTIONS);
        frameLimitSpinner.setSelection(2);
        panel.addView(frameLimitSpinner, matchWrap());
        customFrameLimitEdit = numberField("自定义最大帧数（1–10000）", "1000", false);
        panel.addView(customFrameLimitEdit, fieldParams());

        bitrateLabel = addLabelWithTop(panel, "视频码率", PRIMARY_TEXT);
        bitrateSpinner = createSpinner(BITRATE_OPTIONS);
        panel.addView(bitrateSpinner, matchWrap());
        customBitrateEdit = numberField("自定义码率 Mbps", "8", true);
        panel.addView(customBitrateEdit, fieldParams());

        loopLabel = addLabelWithTop(panel, "GIF 转视频循环次数", PRIMARY_TEXT);
        loopSpinner = createSpinner(LOOP_OPTIONS);
        panel.addView(loopSpinner, matchWrap());
        customLoopEdit = numberField("自定义循环次数（1–100）", "1", false);
        panel.addView(customLoopEdit, fieldParams());

        videoGifOutputLabel = addLabelWithTop(panel, "多视频 GIF 输出", PRIMARY_TEXT);
        videoGifOutputSpinner = createSpinner(VIDEO_GIF_OUTPUT_OPTIONS);
        videoGifOutputSpinner.setSelection(0);
        panel.addView(videoGifOutputSpinner, matchWrap());

        videoLoopLabel = addLabelWithTop(panel, "动画内容重复次数", PRIMARY_TEXT);
        videoLoopSpinner = createSpinner(LOOP_OPTIONS);
        videoLoopSpinner.setSelection(0);
        panel.addView(videoLoopSpinner, matchWrap());
        customVideoLoopEdit = numberField("自定义循环次数（1–100）", "1", false);
        panel.addView(customVideoLoopEdit, fieldParams());

        reverseLoopLabel = addLabelWithTop(panel, "倒放方式", PRIMARY_TEXT);
        reverseLoopSpinner = createSpinner(REVERSE_LOOP_OPTIONS);
        reverseLoopSpinner.setSelection(0);
        panel.addView(reverseLoopSpinner, matchWrap());
        customReverseLoopEdit = numberField("自定义第几次倒放（0=不倒放）", "0", false);
        panel.addView(customReverseLoopEdit, fieldParams());

        gifReplayLabel = addLabelWithTop(panel, "成品 GIF 播放", PRIMARY_TEXT);
        gifReplaySpinner = createSpinner(new String[]{"无限循环", "播放一次"});
        panel.addView(gifReplaySpinner, matchWrap());
        TextView hint = text("重复次数决定动画内容；往返每次包含一轮正放和一轮倒放。成品播放控制保存后的 GIF 是否自动重播。", 12, SECONDARY_TEXT, false);
        hint.setPadding(0, dp(8), 0, dp(4));
        animationOptionsHint = hint;
        panel.addView(hint, matchWrap());

        editButton = createButton("视频 / GIF 剪辑", false);
        panel.addView(editButton);
        editButton.setOnClickListener(v -> {
            if (!hasTimedSourceSelected()) {
                toast("请先添加视频或 GIF");
                return;
            }
            try {
                showAnimationEditor(() -> {
                    updateActionState();
                    toast("剪辑设置已保存");
                });
            } catch (Throwable error) {
                Log.e("FormatConverter", "Unable to open editor", error);
                String type = error.getClass().getSimpleName();
                toast(type.isEmpty() ? "剪辑面板打开失败"
                        : "剪辑面板打开失败：" + type);
            }
        });

        convertButton = createButton("开始转换", true);
        LinearLayout.LayoutParams convertParams = matchWrap();
        convertParams.topMargin = dp(8);
        panel.addView(convertButton, convertParams);
        convertButton.setOnClickListener(v -> beginConversion());

        cancelButton = createButton("取消转换", false);
        cancelButton.setVisibility(View.GONE);
        LinearLayout.LayoutParams cancelParams = matchWrap();
        cancelParams.topMargin = dp(8);
        panel.addView(cancelButton, cancelParams);
        cancelButton.setOnClickListener(v -> cancelActiveTask());

        progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setMax(1000);
        progressBar.setProgress(0);
        progressBar.setVisibility(View.GONE);
        LinearLayout.LayoutParams progressParams = matchWrap();
        progressParams.topMargin = dp(15);
        panel.addView(progressBar, progressParams);

        progressText = text("", 12, SECONDARY_TEXT, false);
        progressText.setGravity(Gravity.CENTER_HORIZONTAL);
        progressText.setVisibility(View.GONE);
        panel.addView(progressText);

        statusText = text("添加文件后会自动判断当前操作是否有效。", 13, SECONDARY_TEXT, false);
        statusText.setGravity(Gravity.CENTER_HORIZONTAL);
        statusText.setPadding(0, dp(12), 0, 0);
        panel.addView(statusText);

        // Detailed helper copy is intentionally omitted; controls explain themselves.
        codecSupportText = text("", 1, SECONDARY_TEXT, false);
        codecSupportText.setVisibility(View.GONE);
        root.addView(codecSupportText, matchWrap());

        AdapterView.OnItemSelectedListener refresh = new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> p, View v, int pos, long id) {
                if (!refreshingOutputFormats) updateControlStates();
            }
            @Override public void onNothingSelected(AdapterView<?> p) { }
        };
        formatSpinner.setOnItemSelectedListener(refresh);
        resolutionSpinner.setOnItemSelectedListener(refresh);
        fpsSpinner.setOnItemSelectedListener(refresh);
        frameLimitSpinner.setOnItemSelectedListener(refresh);
        bitrateSpinner.setOnItemSelectedListener(refresh);
        loopSpinner.setOnItemSelectedListener(refresh);
        videoLoopSpinner.setOnItemSelectedListener(refresh);
        reverseLoopSpinner.setOnItemSelectedListener(refresh);
        gifReplaySpinner.setOnItemSelectedListener(refresh);
        videoGifOutputSpinner.setOnItemSelectedListener(refresh);

        TextWatcher watcher = new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) { }
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) {
                updateActionState();
                scheduleRecommendation();
            }
            @Override public void afterTextChanged(Editable s) { }
        };
        customWidthEdit.addTextChangedListener(watcher);
        customHeightEdit.addTextChangedListener(watcher);
        customFpsEdit.addTextChangedListener(watcher);
        customFrameLimitEdit.addTextChangedListener(watcher);
        customBitrateEdit.addTextChangedListener(watcher);
        customLoopEdit.addTextChangedListener(watcher);
        customVideoLoopEdit.addTextChangedListener(watcher);
        customReverseLoopEdit.addTextChangedListener(watcher);

        setContentView(scroll);
        refreshCodecSupportText();
        updateControlStates();
        updateSelectionUi();
    }

    private int selectedOutputFormat() {
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

    private void updateControlStates() {
        if (formatSpinner == null) return;
        int format = selectedOutputFormat();
        if (format < 0) {
            setViewsVisible(false, qualityText, qualitySeek, resolutionLabel, resolutionSpinner,
                    resolutionCustomRow, fpsLabel, fpsSpinner, customFpsEdit, frameLimitLabel,
                    frameLimitSpinner, customFrameLimitEdit, bitrateLabel, bitrateSpinner,
                    customBitrateEdit, loopLabel, loopSpinner, customLoopEdit, videoGifOutputLabel,
                    videoGifOutputSpinner, videoLoopLabel, videoLoopSpinner, customVideoLoopEdit,
                    reverseLoopLabel, reverseLoopSpinner, customReverseLoopEdit, gifReplayLabel, gifReplaySpinner, animationOptionsHint);
            boolean canManualEdit = hasTimedSourceSelected();
            setViewsVisible(canManualEdit, editButton);
            if (editButton != null) {
                editButton.setEnabled(!busy && canManualEdit);
                applyEditButtonStyle(editButton, !busy && canManualEdit);
            }
            recommendationText.setText("当前文件组合没有可用输出格式");
            updateActionState();
            return;
        }
        boolean jpeg = format == 0;
        boolean png = format == 1;
        boolean bmp = format == 2;
        boolean gif = format == 3;
        boolean video = format >= 4 && format <= 6;
        boolean lossyWebp = format == 7;
        boolean losslessWebp = format == 8;
        boolean mp3 = format == 9;
        boolean m4a = format == 10;
        boolean pdfOut = format == 11;
        boolean icoOut = format == 12;
        boolean textOut = isTextOutputFormat(format);
        boolean textPdfOut = format == 23;
        boolean audio = mp3 || m4a || format == 27;
        boolean animated = gif || video;
        boolean videoGifMode = gif && hasOnlyVideosSelected();
        boolean multiVideoGifMode = videoGifMode && selectedItems.size() > 1;
        boolean gifEditMode = videoGifMode || (gif && selectedItems.size() == 1
                && selectedItems.get(0).sourceFormat == SourceFormat.GIF);
        boolean imageQuality = jpeg || lossyWebp || pdfOut;
        boolean hideMediaControls = audio || textOut;
        int resolutionPosition = resolutionSpinner.getSelectedItemPosition();
        int fpsPosition = fpsSpinner.getSelectedItemPosition();
        int frameLimitPosition = frameLimitSpinner.getSelectedItemPosition();
        int bitratePosition = bitrateSpinner.getSelectedItemPosition();
        int loopPosition = loopSpinner.getSelectedItemPosition();
        int videoLoopPosition = videoLoopSpinner.getSelectedItemPosition();
        int reverseLoopPosition = reverseLoopSpinner.getSelectedItemPosition();

        // Remove irrelevant controls from the layout instead of leaving disabled rows that the
        // user must scroll past. Custom fields are also only present while their option is active.
        setViewsVisible(imageQuality, qualityText, qualitySeek);
        setViewsVisible(!hideMediaControls, resolutionLabel, resolutionSpinner);
        setViewsVisible(!hideMediaControls && resolutionPosition == 7, resolutionCustomRow);
        setViewsVisible(animated, fpsLabel, fpsSpinner);
        setViewsVisible(animated && fpsPosition == 8, customFpsEdit);
        setViewsVisible(animated, frameLimitLabel, frameLimitSpinner);
        setViewsVisible(animated && frameLimitPosition == 5, customFrameLimitEdit);
        setViewsVisible(video, bitrateLabel, bitrateSpinner);
        setViewsVisible(video && bitratePosition == 7, customBitrateEdit);
        setViewsVisible(video, loopLabel, loopSpinner);
        setViewsVisible(video && loopPosition == 5, customLoopEdit);
        setViewsVisible(multiVideoGifMode, videoGifOutputLabel, videoGifOutputSpinner);
        setViewsVisible(gifEditMode, videoLoopLabel, videoLoopSpinner);
        setViewsVisible(gifEditMode && videoLoopPosition == 5, customVideoLoopEdit);
        setViewsVisible(gifEditMode, reverseLoopLabel, reverseLoopSpinner);
        setViewsVisible(gifEditMode && reverseLoopPosition == 6, customReverseLoopEdit);
        boolean canManualEdit = hasTimedSourceSelected();
        setViewsVisible(gifEditMode, animationOptionsHint);
        setViewsVisible(gif, gifReplayLabel, gifReplaySpinner);
        gifReplaySpinner.setEnabled(gif && !busy);
        setViewsVisible(canManualEdit, editButton);

        if (!busy) {
            boolean smartQuality = resolutionPosition == 0;
            qualitySeek.setEnabled(((jpeg || lossyWebp || pdfOut) && !smartQuality)
                    || textPdfOut);
            resolutionSpinner.setEnabled(!hideMediaControls);
            fpsSpinner.setEnabled(animated);
            frameLimitSpinner.setEnabled(animated);
            bitrateSpinner.setEnabled(video);
            loopSpinner.setEnabled(video);
            videoLoopSpinner.setEnabled(gifEditMode);
            reverseLoopSpinner.setEnabled(gifEditMode);
            videoGifOutputSpinner.setEnabled(multiVideoGifMode);

            customWidthEdit.setEnabled(!hideMediaControls && resolutionPosition == 7);
            customHeightEdit.setEnabled(!hideMediaControls && resolutionPosition == 7);
            customFpsEdit.setEnabled(animated && fpsPosition == 8);
            customFrameLimitEdit.setEnabled(animated && frameLimitPosition == 5);
            customBitrateEdit.setEnabled(video && bitratePosition == 7);
            customLoopEdit.setEnabled(video && loopPosition == 5);
            customVideoLoopEdit.setEnabled(gifEditMode && videoLoopPosition == 5);
            customReverseLoopEdit.setEnabled(gifEditMode && reverseLoopPosition == 6);
            if (editButton != null) {
                editButton.setEnabled(canManualEdit);
                editButton.setText("视频 / GIF 剪辑");
                applyEditButtonStyle(editButton, canManualEdit);
            }
        }

        if (png) qualityText.setText("PNG 为无损格式，质量滑块不生效");
        else if (bmp) qualityText.setText("BMP 基本不压缩，质量滑块不生效");
        else if (gif) qualityText.setText("GIF 使用有限色彩调色板，质量滑块不生效");
        else if (format == 4) qualityText.setText("H.264：兼容优先，画质由分辨率和码率决定");
        else if (format == 5) qualityText.setText("H.265：更省空间，画质由分辨率和码率决定");
        else if (format == 6) qualityText.setText("AV1：压缩率更高，但编码可能更慢");
        else if (losslessWebp) qualityText.setText("WebP 无损模式，质量滑块不生效");
        else if (mp3) qualityText.setText("MP3：192 kbps 高质量立体声，自动下混多声道");
        else if (m4a) qualityText.setText("M4A：AAC 原音轨直接提取，不降低音质");
        else if (icoOut) qualityText.setText("ICO 内嵌无损 PNG 帧，质量滑块不生效");
        else if (textPdfOut) {
            qualityText.setText("文本 PDF：矢量文字，可选择与复制，无损清晰");
        }
        else if (textOut) qualityText.setText("文本转换不涉及画质，无需质量与分辨率设置");
        else if (pdfOut && resolutionPosition == 0) {
            qualityText.setText("PDF 图片页：JPEG 质量 " + qualitySeek.getProgress() + "/100");
        }
        else if (resolutionPosition == 0) {
            qualityText.setText("智能质量：按原图细节和压缩程度自动调整");
        } else {
            qualityText.setText("图片质量：" + qualitySeek.getProgress()
                    + (qualityTouched ? "（已调整）" : ""));
        }


        updateActionState();
        scheduleRecommendation();
    }

    /** Debounced background probing; UI reads are captured before submitting the worker. */
    private void scheduleRecommendation() {
        if (recommendationText == null || busy || isDestroyed()) return;
        int generation=++recommendationGeneration;
        recommendationHandler.removeCallbacksAndMessages(null);
        if(recommendationTask!=null)recommendationTask.cancel(true);
        if(selectedItems.isEmpty()){recommendationText.setText("添加文件后显示推荐数值");return;}
        final List<SelectedItem> items=new ArrayList<>(selectedItems);
        final int format=selectedOutputFormat();
        if (format < 0) { recommendationText.setText("当前文件组合没有可用输出格式"); return; }
        final int resolution=resolutionSpinner.getSelectedItemPosition();
        final int fps=selectedFps(),limit=selectedFrameLimit(),bitrate=selectedBitrate(),quality=qualitySeek.getProgress();
        final int repetitions = selectedVideoLoops(), reverseMode = selectedReverseLoop();
        final int loops=format==3?GifPlaybackPlan.passCount(repetitions, reverseMode):selectedLoops();
        final int[] bounds=selectedBounds(0,0,format==3);
        final AnimationEdits edits=animationEdits==null?freshAnimationEdits():animationEdits;
        if(isTextOutputFormat(format)){
            recommendationText.setText(format==23?"PDF：A4 595×842 pt · 字号 11 pt · 行距 1.42 · 可选择文字":"文档输出：UTF-8；DOCX / EPUB / ODT 提取正文，复杂版式不保留");return;
        }
        if(format==9||format==10||format==27){recommendationText.setText(format==9?"MP3：单声道 128 kbps / 双声道 192 kbps":format==10?"M4A：AAC 原码率复制；其他编码转为 48 kHz / 双声道 / 192 kbps":"WAV：48 kHz / 16 bit / 双声道 · 约 11.52 MB/分钟");return;}
        recommendationText.setText("正在计算推荐数值……");
        recommendationHandler.postDelayed(()->recommendationTask=recommendationExecutor.submit(()->{
            Bitmap sample=null;
            try {
                SelectedItem first=items.get(0);int width,height;double seconds=0, fpsHint=-1;int[] target=bounds;
                String extra="";int q=quality;
                if(first.isVideo()) {
                    List<VideoFrameDecoder.Info> infos=new ArrayList<>();List<Long> starts=new ArrayList<>(),ends=new ArrayList<>();
                    for(SelectedItem item:items){if(Thread.currentThread().isInterrupted())return;VideoFrameDecoder.Info info=VideoFrameDecoder.probe(this,item.uri);infos.add(info);long start=Math.min(Math.round(edits.trimStartSeconds*1e6),Math.max(0,info.durationUs-1));long end=edits.trimDurationSeconds<=0?info.durationUs:Math.min(info.durationUs,start+Math.round(edits.trimDurationSeconds*1e6));starts.add(start);ends.add(end);}
                    VideoTimeline timeline=buildVideoTimeline(items,infos,starts,ends,edits);
                    for(int i=0;i<timeline.items.size();i++)seconds+=(timeline.endsUs.get(i)-timeline.startsUs.get(i))/1e6/edits.speed;
                    seconds*=loops;
                    width=infos.get(0).orientedWidth();height=infos.get(0).orientedHeight();
                    if(format==3&&resolution==0&&!timeline.items.isEmpty())target=smartVideoGifBounds(timeline.items,timeline.infos,timeline.startsUs,timeline.endsUs,Math.min(limit,(long)Math.ceil(seconds*fps)));
                } else if(first.sourceFormat==SourceFormat.GIF) {
                    GifDrawable info = new GifDrawable(getContentResolver(), first.uri);
                    try {
                        info.stop(); width=Math.max(1,info.getIntrinsicWidth()); height=Math.max(1,info.getIntrinsicHeight());
                        double duration=Math.max(1,info.getDuration())/1000.0;
                        double start=Math.min(Math.max(0,edits.trimStartSeconds),Math.max(0,duration-.001));
                        double end=edits.trimDurationSeconds<=0?duration:Math.min(duration,start+edits.trimDurationSeconds);
                        double kept=edits.keptDurationSeconds(start,end)/edits.speed;
                        if(format==3) {
                            GifPlaybackPlan plan=new GifPlaybackPlan(kept,fps,limit,repetitions,reverseMode);
                            seconds=plan.totalSeconds;fpsHint=plan.actualFps;
                            if(resolution==0) {
                                int[] edited=FrameEditor.editedSize(width,height,edits);
                                target=smartAnimatedGifBounds(edited[0],edited[1],
                                        (int)Math.max(1,Math.min(Integer.MAX_VALUE,Math.round(seconds*1000))),plan.totalFrames,first.size);
                            }
                        } else if(format>=4&&format<=6) seconds=kept*loops;
                        extra=" · 原图 "+width+"×"+height;
                    } finally {info.recycle();}
                } else if(first.sourceFormat==SourceFormat.PDF) {
                    try(ParcelFileDescriptor fd=getContentResolver().openFileDescriptor(first.uri,"r");PdfRenderer pdf=new PdfRenderer(fd);PdfRenderer.Page page=pdf.openPage(0)) {
                        int[] size=pdfRenderTargetSize(page.getWidth(),page.getHeight(),resolution,bounds[0],bounds[1],memorySafePixelCap());width=size[0];height=size[1];target=size;extra=" · "+pdf.getPageCount()+" 页";
                    }
                } else if(isTextSourceFormat(first.sourceFormat)||first.sourceFormat==SourceFormat.AUDIO) return;
                else {
                    String extraKind=ExtraImageFormats.kind(this,first.uri);
                    if(!extraKind.isEmpty()) {
                        final String result="扩展图片："+extraKind+" → "+outputSpec(format).shortName+"；当前边界 "+bounds[0]+"×"+bounds[1]+"，保留纵横比；实际尺寸在导出时显示。";
                        runOnUiThread(()->{if(!isDestroyed()&&!busy&&generation==recommendationGeneration)recommendationText.setText(result);});
                        return;
                    }
                    int[] sourceSize=new int[2];
                    sample=ImageDecoder.decodeBitmap(ImageDecoder.createSource(getContentResolver(),first.uri),(decoder,info,source)->{
                        sourceSize[0]=info.getSize().getWidth();sourceSize[1]=info.getSize().getHeight();decoder.setAllocator(ImageDecoder.ALLOCATOR_SOFTWARE);decoder.setTargetSize(Math.min(72,sourceSize[0]),Math.min(72,sourceSize[1]));
                    });width=sourceSize[0];height=sourceSize[1];
                    if(format==3&&resolution==0&&first.sourceFormat!=SourceFormat.GIF)target=smartImageGifBounds(sample,Math.min(items.size(),limit),fps);
                    if(format==3&&first.sourceFormat==SourceFormat.GIF)extra=" · 动画时长与帧数在导出时复核";
                    int[] imageSize=fitSize(width,height,bounds[0],bounds[1],true);
                    if(resolution==0&&(format==0||format==7))q=qualityForProfile(first,analyzeImage(sample),format,(long)imageSize[0]*imageSize[1]);
                }
                if(format>=3&&format<=6){int[] edited=FrameEditor.editedSize(width,height,edits);width=edited[0];height=edited[1];}
                int[] size=fitSize(width,height,target[0],target[1],true);
                String message=(resolution==0?"智能推荐（预计）：":"当前设置（预计）：")+size[0]+"×"+size[1];
                if(format==0||format==7||format==11)message+=" · 质量 "+q+"/100";
                if(format==3||(format>=4&&format<=6)) {
                    double actual=fpsHint>0?fpsHint:seconds>0?Math.min(format==3?Math.min(100,fps):fps,limit/seconds):fps;
                    message+=String.format(Locale.CHINA," · %.2f FPS · 上限 %d 帧",actual,limit);
                    if(seconds>0)message+=String.format(Locale.CHINA," · %.2f 秒",seconds);
                    if(format>=4&&format<=6){int rate=bitrate>0?bitrate:Mp4Encoder.autoBitrate(videoCodecSpec(format).mime,size[0],size[1],Math.max(1,(int)Math.round(actual)));message+=String.format(Locale.CHINA," · %s %.2f Mbps",bitrate==0?"自动码率":"码率",rate/1e6);}
                }
                if(items.size()>1)message+=" · 首项尺寸 / 共 "+items.size()+" 项";
                final String result=message+extra+"\n实际导出会按设备能力与剩余内存复核。";
                runOnUiThread(()->{if(!isDestroyed()&&!busy&&generation==recommendationGeneration)recommendationText.setText(result);});
            } catch(Exception error){runOnUiThread(()->{if(!isDestroyed()&&!busy&&generation==recommendationGeneration)recommendationText.setText("暂未读到推荐参数："+safeMessage(error));});}
            finally{if(sample!=null)sample.recycle();}
        }),250);
    }

    private void handleIncomingShareIntent(Intent intent) {
        if (intent == null || busy) return;
        String action = intent.getAction();
        if (!Intent.ACTION_SEND.equals(action)
                && !Intent.ACTION_SEND_MULTIPLE.equals(action)) return;

        List<Uri> sharedUris = new ArrayList<>();
        try {
            if (Intent.ACTION_SEND_MULTIPLE.equals(action)) {
                ArrayList<Uri> streams = intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM);
                if (streams != null) sharedUris.addAll(streams);
            } else {
                Uri stream = intent.getParcelableExtra(Intent.EXTRA_STREAM);
                if (stream != null) sharedUris.add(stream);
            }
        } catch (Exception ignored) { }

        ClipData clip = intent.getClipData();
        if (clip != null) {
            for (int i = 0; i < clip.getItemCount(); i++) {
                Uri uri = clip.getItemAt(i).getUri();
                if (uri != null && !sharedUris.contains(uri)) sharedUris.add(uri);
            }
        }
        Uri data = intent.getData();
        if (data != null && !sharedUris.contains(data)) sharedUris.add(data);

        int added = 0;
        int flags = intent.getFlags() & (Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        for (Uri uri : sharedUris) {
            if (addSelectedUri(uri, flags)) added++;
        }
        if (added <= 0) return;

        updateSelectionUi();
        if (hasOnlyVideosSelected() && formatSpinner != null) {
            // Gallery -> app should land on a useful video conversion mode immediately.
            setSelectedOutputFormat(3);
        }
        toast(added == 1 ? "已从相册接收文件" : "已从相册接收 " + added + " 个文件");
    }

    private void openFilePicker() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*");
        intent.putExtra(Intent.EXTRA_MIME_TYPES,
                new String[]{"image/*", "video/*", "audio/*", "application/pdf", "text/*",
                        "application/epub+zip", "application/vnd.oasis.opendocument.text",
                        "application/rtf", "application/x-ndjson", "application/x-fictionbook+xml", "application/octet-stream",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "application/json", "application/yaml", "application/x-yaml",
                        "application/xml", "text/xml", "application/x-subrip"});
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        startActivityForResult(intent, REQUEST_PICK);
    }

    @Override
    @SuppressWarnings("deprecation")
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_MUSIC) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null) {
                backgroundMusic = data.getData();
                try { getContentResolver().takePersistableUriPermission(backgroundMusic,
                        data.getFlags() & Intent.FLAG_GRANT_READ_URI_PERMISSION); } catch (Exception ignored) { }
                if (activeEditorDialog != null && activeEditorDialog.isShowing()) showAudioSettings();
            }
            return;
        }
        if (requestCode == REQUEST_PICK && resultCode == RESULT_OK && data != null) {
            receivePickedFiles(data);
            return;
        }
        if (requestCode == REQUEST_SAVE) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null) {
                savePendingFile(data.getData());
            } else {
                cleanupPending();
                setBusy(false);
                statusText.setText("已取消保存。转换缓存已清理。");
            }
            return;
        }
        if (requestCode == REQUEST_SAVE_FOLDER) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null) {
                Uri treeUri = data.getData();
                int takeFlags = data.getFlags()
                        & (Intent.FLAG_GRANT_READ_URI_PERMISSION
                        | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                try {
                    getContentResolver().takePersistableUriPermission(treeUri, takeFlags);
                } catch (Exception ignored) { }
                savePendingBatchToFolder(treeUri);
            } else {
                cleanupPending();
                setBusy(false);
                statusText.setText("已取消选择保存文件夹。转换缓存已清理。");
            }
        }
    }

    private void receivePickedFiles(Intent data) {
        int firstNewIndex = selectedItems.size();
        int added = 0;
        int duplicates = 0;
        ClipData clips = data.getClipData();
        if (clips != null) {
            for (int i = 0; i < clips.getItemCount(); i++) {
                if (addSelectedUri(clips.getItemAt(i).getUri(), data.getFlags())) added++;
                else duplicates++;
            }
        } else if (data.getData() != null) {
            if (addSelectedUri(data.getData(), data.getFlags())) added++;
            else duplicates++;
        }
        updateSelectionUi();
        if (added > 0) {
            toast("已新增 " + added + " 个文件" + (duplicates > 0 ? "，跳过重复 " + duplicates + " 个" : ""));
            boolean importedVideo = false;
            for (int i = firstNewIndex; i < selectedItems.size(); i++) {
                if (selectedItems.get(i).isVideo()) { importedVideo = true; break; }
            }
            if (importedVideo) {
                // Wait for the picker to return and the Activity window to be attached.
                selectedRecycler.post(() -> {
                    if (isFinishing() || isDestroyed() || busy || activeEditorDialog != null) return;
                    try { showAnimationEditor(this::updateActionState); }
                    catch (RuntimeException error) {
                        Log.e("FormatConverter", "Unable to open imported video", error);
                        toast("剪辑窗口暂时无法打开，请点视频 / GIF 剪辑重试");
                    }
                });
            }
        } else if (duplicates > 0) {
            toast("这些文件已经在列表中");
        } else {
            toast("没有读取到文件");
        }
    }

    private boolean addSelectedUri(Uri uri, int flags) {
        if (uri == null) return false;
        for (SelectedItem item : selectedItems) {
            if (item.uri.equals(uri)) return false;
        }
        String name = queryDisplayName(uri);
        String mime = getContentResolver().getType(uri);
        long size = queryFileSize(uri);
        SourceFormat sourceFormat = detectSourceFormat(uri, name, mime);
        selectedItems.add(new SelectedItem(uri, name, mime, size, sourceFormat));
        animationEdits = freshAnimationEdits();
        int takeFlags = flags & Intent.FLAG_GRANT_READ_URI_PERMISSION;
        if (takeFlags != 0) {
            try {
                getContentResolver().takePersistableUriPermission(uri, takeFlags);
            } catch (Exception ignored) { }
        }
        selectedAdapter.notifyItemInserted(selectedItems.size() - 1);
        return true;
    }

    private void beginConversion() {
        ActionState action = evaluateActionState();
        if (!action.enabled) {
            toast(action.reason);
            return;
        }
        continueBeginConversion();
    }

    private void continueBeginConversion() {
        ActionState action = evaluateActionState();
        if (!action.enabled || busy) return;

        int selectedFormat = selectedOutputFormat();
        boolean staticBatch = isStaticOutputFormat(selectedFormat) && selectedItems.size() > 1;
        if (staticBatch && selectedItems.size() > ZIP_SUGGEST_THRESHOLD) {
            new AlertDialog.Builder(this)
                    .setTitle("图片数量较多")
                    .setMessage("已选择 " + selectedItems.size()
                            + " 张图片。打包 ZIP 保存更快，也方便一次分享；也可以仍然分别保存到一个文件夹。")
                    .setPositiveButton("打包 ZIP（推荐）",
                            (dialog, which) -> beginConversionInternal(BatchMode.ZIP))
                    .setNegativeButton("分别保存",
                            (dialog, which) -> beginConversionInternal(BatchMode.SEPARATE))
                    .setNeutralButton("取消", null)
                    .show();
            return;
        }
        boolean pdfPageBatch = !staticBatch
                && isPdfToStaticImagesMode(selectedFormat, selectedItems);
        if (pdfPageBatch) {
            int pageCount = countPdfPagesSafe(selectedItems.get(0).uri);
            if (pageCount > ZIP_SUGGEST_THRESHOLD) {
                new AlertDialog.Builder(this)
                        .setTitle("PDF 页数较多")
                        .setMessage("这个 PDF 共 " + pageCount
                                + " 页。打包 ZIP 保存更快，也方便一次分享；也可以把每页分别保存到一个文件夹。")
                        .setPositiveButton("打包 ZIP（推荐）",
                                (dialog, which) -> beginConversionInternal(BatchMode.ZIP))
                        .setNegativeButton("分别保存",
                                (dialog, which) -> beginConversionInternal(BatchMode.SINGLE))
                        .setNeutralButton("取消", null)
                        .show();
                return;
            }
            beginConversionInternal(BatchMode.SINGLE);
            return;
        }
        if (isTextOutputFormat(selectedFormat) && selectedItems.size() > 1) {
            if (selectedItems.size() > ZIP_SUGGEST_THRESHOLD) {
                new AlertDialog.Builder(this)
                        .setTitle("文本文件较多")
                        .setMessage("已选择 " + selectedItems.size()
                                + " 个文本文件。打包 ZIP 保存更快，也方便一次分享；也可以把每个转换结果分别保存到一个文件夹。")
                        .setPositiveButton("打包 ZIP（推荐）",
                                (dialog, which) -> beginConversionInternal(BatchMode.ZIP))
                        .setNegativeButton("分别保存",
                                (dialog, which) -> beginConversionInternal(BatchMode.SEPARATE))
                        .setNeutralButton("取消", null)
                        .show();
                return;
            }
            beginConversionInternal(BatchMode.SEPARATE);
            return;
        }
        if (selectedFormat == 12 && selectedItems.size() > 1) {
            if (selectedItems.size() > ZIP_SUGGEST_THRESHOLD) {
                new AlertDialog.Builder(this)
                        .setTitle("图标数量较多")
                        .setMessage("已选择 " + selectedItems.size()
                                + " 张图片。打包 ZIP 保存更快，也方便一次分享；也可以把每个图标分别保存到一个文件夹。")
                        .setPositiveButton("打包 ZIP（推荐）",
                                (dialog, which) -> beginConversionInternal(BatchMode.ZIP))
                        .setNegativeButton("分别保存",
                                (dialog, which) -> beginConversionInternal(BatchMode.SEPARATE))
                        .setNeutralButton("取消", null)
                        .show();
                return;
            }
            beginConversionInternal(BatchMode.SEPARATE);
            return;
        }
        beginConversionInternal(staticBatch ? BatchMode.SEPARATE : BatchMode.SINGLE);
    }

    private void showAnimationEditor(Runnable afterSave) {
        if (busy || activeEditorDialog != null || isFinishing() || isDestroyed()) return;
        final List<SelectedItem> editorItems = new ArrayList<>();
        for (SelectedItem item : selectedItems) if (item.isVideo()) editorItems.add(item);
        if (editorItems.isEmpty()) {
            for (SelectedItem item : selectedItems) {
                if (item.sourceFormat == SourceFormat.GIF) { editorItems.add(item); break; }
            }
        }
        if (editorItems.isEmpty()) { toast("请先添加视频或 GIF"); return; }
        final Uri savedMusic = backgroundMusic;
        final float savedOriginalVolume = originalVolume, savedMusicVolume = musicVolume;
        final boolean savedMusicLoop = musicLoop;
        final double savedMusicStart = musicStartSeconds, savedAudioFade = audioFadeSeconds;
        final boolean[] editsCommitted = {false};
        final AnimationEdits current = animationEdits == null
                ? freshAnimationEdits() : animationEdits;
        final double timelineSeconds = Math.max(0.1, estimateEditTimelineSeconds(editorItems));
        final List<AnimationEdits.TimeRange> deletedRanges =
                new ArrayList<>(current.deletedRanges);
        final List<AnimationEdits.TimeRange> reversedRanges =
                new ArrayList<>(current.reversedRanges);

        ScrollView scroll = new ScrollView(this);
        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(12), dp(4), dp(12), dp(10));
        scroll.addView(content, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));

        // Segment gaps and source clip borders are visual, so no helper sentence is needed.

        final double[] splitPoints = {Double.NaN, Double.NaN};
        final java.util.ArrayDeque<EditorTimelineState> undoHistory =
                new java.util.ArrayDeque<>();
        final java.util.ArrayDeque<EditorTimelineState> redoHistory =
                new java.util.ArrayDeque<>();

        final EditorVideoPlayer[] videoPreview = {null};
        final ImageView[] gifPreviewView = {null};
        final GifDrawable[] gifPreview = {null};
        final int[] previewVideoIndex = {-1};
        final double[] previewVideoOffsetSeconds = {0.0};
        final double[] previewVideoDurations = new double[editorItems.size()];
        final long[] pendingVideoSeekMs = {0L};
        final boolean[] playWanted = {false};
        final boolean[] editorClosed = {false};
        final boolean[] timelineDragging = {false};
        final boolean separateVideoPreviews = false; // Editor and direct MP4 export use one timeline.

        final int[] previewCropMode = {current.cropMode};
        final int[] previewRotation = {current.rotationDegrees};
        final boolean[] previewFlipHorizontal = {current.flipHorizontal};
        final boolean[] previewFlipVertical = {current.flipVertical};
        final int[] previewBrightness = {current.brightness};
        final int[] previewContrast = {current.contrast};
        final int[] previewSaturation = {current.saturation};
        final AnimationEdits[] previewVisualEdits = {new AnimationEdits(
                0, 0, 1.0,
                previewCropMode[0], previewRotation[0],
                previewFlipHorizontal[0], previewFlipVertical[0],
                previewBrightness[0], previewContrast[0], previewSaturation[0],
                deletedRanges, reversedRanges)};

        FrameLayout previewFrame = new FrameLayout(this);
        previewFrame.setBackgroundColor(0xFF111111);
        LinearLayout.LayoutParams previewParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(228));
        content.addView(previewFrame, previewParams);

        if (hasOnlyVideos(editorItems)) {
            try {
                for (int i = 0; i < editorItems.size(); i++) {
                    previewVideoDurations[i] = Math.max(
                            0.1, videoDurationSeconds(editorItems.get(i)));
                }
                EditorVideoPlayer preview = new EditorVideoPlayer(this);
                videoPreview[0] = preview;
                preview.setBackgroundColor(0xFF111111);
                preview.setContentDescription("视频剪辑预览");
                previewVideoIndex[0] = 0;
                preview.setExpectedDurationMs((int) Math.min(Integer.MAX_VALUE,
                        Math.round(previewVideoDurations[0] * 1000.0)));
                preview.setOnPreparedListener(player -> {
                    if (editorClosed[0]) return;
                    int duration = Math.max(1, player.getDuration());
                    int seek = (int) Math.min(duration - 1L,
                            Math.max(0L, pendingVideoSeekMs[0]));
                    if (seek > 0) preview.seekTo(seek);
                    if (playWanted[0]) preview.start();
                });
                preview.setOnCompletionListener(player -> {
                    if (editorClosed[0]) return;
                    if (!separateVideoPreviews
                            && previewVideoIndex[0] >= 0
                            && previewVideoIndex[0] + 1 < editorItems.size()
                            && playWanted[0]) {
                        int next = previewVideoIndex[0] + 1;
                        previewVideoOffsetSeconds[0] +=
                                previewVideoDurations[previewVideoIndex[0]];
                        previewVideoIndex[0] = next;
                        pendingVideoSeekMs[0] = 0L;
                        preview.setExpectedDurationMs((int) Math.min(Integer.MAX_VALUE,
                                Math.round(previewVideoDurations[next] * 1000.0)));
                        preview.setVideoURI(editorItems.get(next).uri);
                        preview.start();
                    } else {
                        playWanted[0] = false;
                    }
                });
                preview.setVideoURI(editorItems.get(0).uri);
                preview.seekTo(1);
                previewFrame.addView(preview, new FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT));
                preview.applyVisualEdits(previewVisualEdits[0]);
            } catch (Throwable previewError) {
                Log.e("FormatConverter", "Video editor preview unavailable", previewError);
                if (videoPreview[0] != null) {
                    try { videoPreview[0].stopPlayback(); } catch (Throwable ignored) { }
                }
                videoPreview[0] = null;
                previewVideoIndex[0] = -1;
                previewFrame.removeAllViews();
                TextView previewFallback = text(
                        "当前视频无法生成预览，但仍可拖动时间轴并保存剪辑设置。",
                        12, 0xFFD7D8DE, false);
                previewFallback.setGravity(Gravity.CENTER);
                previewFrame.addView(previewFallback, new FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT));
            }
        } else if (editorItems.size() == 1
                && editorItems.get(0).sourceFormat == SourceFormat.GIF) {
            try {
                GifDrawable drawable = new GifDrawable(
                        getContentResolver(), editorItems.get(0).uri);
                ImageView preview = new ImageView(this);
                preview.setScaleType(ImageView.ScaleType.FIT_CENTER);
                preview.setBackgroundColor(0xFF111111);
                preview.setImageDrawable(drawable);
                preview.setContentDescription("GIF 剪辑预览");
                drawable.stop();
                drawable.seekTo(0);
                previewFrame.addView(preview, new FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT));
                gifPreviewView[0] = preview;
                gifPreview[0] = drawable;
            } catch (Exception ignored) { }
        }

        TextView audioStatus = text("", 1, SECONDARY_TEXT, false);
        audioStatus.setVisibility(View.GONE);
        if (videoPreview[0] != null) {
            videoPreview[0].setAudioStatusListener(audioStatus::setText);
            videoPreview[0].setPreviewVolume(originalVolume);
        } else audioStatus.setText("GIF 本身没有原声，可在声音设置中添加配乐。");
        Button editorAudio = createButton("声音设置 / 添加背景音乐", false);
        content.addView(editorAudio, matchWrap());
        editorAudio.setOnClickListener(v -> {
            if (pauseEditorPreview != null) pauseEditorPreview.run();
            showAudioSettings();
        });
        refreshEditorAudio = () -> {
            if (videoPreview[0] != null) {
                videoPreview[0].setPreviewVolume(originalVolume);
                videoPreview[0].setBackgroundMusic(backgroundMusic, musicVolume, musicLoop,
                        musicStartSeconds, audioFadeSeconds);
            }
            editorAudio.setText(backgroundMusic == null ? "声音设置 / 添加背景音乐"
                    : "声音设置 · 已添加背景音乐");
        };
        refreshEditorAudio.run();

        final List<Double> sourceClipBoundaries = new ArrayList<>();
        if (previewVideoDurations.length > 1) {
            double sourceCursor = 0.0;
            for (int i = 0; i < previewVideoDurations.length - 1; i++) {
                sourceCursor += Math.max(0.0, previewVideoDurations[i]);
                if (sourceCursor > 0.01 && sourceCursor < timelineSeconds - 0.01) {
                    sourceClipBoundaries.add(sourceCursor);
                }
            }
        }

        final EditorTimelineView timeline = new EditorTimelineView(this);
        timeline.setDurationSeconds(timelineSeconds);
        timeline.setSourceBoundaries(sourceClipBoundaries);
        timeline.setPositionSeconds(0.0);
        timeline.setSplitPoints(splitPoints[0], splitPoints[1]);
        timeline.setRanges(deletedRanges, reversedRanges);

        final Button playPauseButton = createEditorButton("▶", true);
        playPauseButton.setContentDescription("播放");
        if (hasOnlyVideos(editorItems) && videoPreview[0] == null) {
            playPauseButton.setEnabled(false);
            applyEditorButtonStyle(playPauseButton, false, true);
        }
        final TextView timeText = text(
                "0:00.00 / " + formatTimelineTime(timeline.getVisibleDurationSeconds()),
                11, 0xFFFFFFFF, true);
        timeText.setGravity(Gravity.CENTER_VERTICAL);

        LinearLayout bottomOverlay = new LinearLayout(this);
        bottomOverlay.setOrientation(LinearLayout.VERTICAL);
        bottomOverlay.setPadding(dp(8), dp(5), dp(8), dp(3));
        bottomOverlay.setBackgroundColor(0x99000000);

        LinearLayout transportRow = new LinearLayout(this);
        transportRow.setOrientation(LinearLayout.HORIZONTAL);
        transportRow.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout.LayoutParams playParams = new LinearLayout.LayoutParams(dp(42), dp(36));
        playParams.setMarginEnd(dp(8));
        transportRow.addView(playPauseButton, playParams);
        transportRow.addView(timeText, new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        bottomOverlay.addView(transportRow, matchWrap());
        bottomOverlay.addView(timeline, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));

        FrameLayout.LayoutParams overlayParams = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT,
                Gravity.BOTTOM);
        previewFrame.addView(bottomOverlay, overlayParams);

        final Handler editorHandler = new Handler(Looper.getMainLooper());

        final Runnable[] updatePreviewVisual = new Runnable[1];
        updatePreviewVisual[0] = () -> {
            previewVisualEdits[0] = new AnimationEdits(
                    0, 0, 1.0,
                    previewCropMode[0], previewRotation[0],
                    previewFlipHorizontal[0], previewFlipVertical[0],
                    previewBrightness[0], previewContrast[0], previewSaturation[0],
                    deletedRanges, reversedRanges);

            if (gifPreviewView[0] != null) {
                Paint previewPaint = FrameEditor.createPaint(previewVisualEdits[0]);
                gifPreviewView[0].setColorFilter(previewPaint.getColorFilter());
                gifPreviewView[0].setRotation(previewRotation[0]);
                gifPreviewView[0].setScaleX(previewFlipHorizontal[0] ? -1f : 1f);
                gifPreviewView[0].setScaleY(previewFlipVertical[0] ? -1f : 1f);
                gifPreviewView[0].setScaleType(previewCropMode[0] == AnimationEdits.CROP_NONE
                        ? ImageView.ScaleType.FIT_CENTER : ImageView.ScaleType.CENTER_CROP);
            }

            if (videoPreview[0] != null) {
                videoPreview[0].applyVisualEdits(previewVisualEdits[0]);
            }
        };

        final java.util.function.DoubleConsumer seekPreviewTo = secondsValue -> {
            double seconds = Math.max(0.0, Math.min(timelineSeconds, secondsValue));
            for (AnimationEdits.TimeRange deleted : deletedRanges) {
                if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {
                    seconds = deleted.endSeconds < timelineSeconds
                            ? deleted.endSeconds : Math.max(0.0, deleted.startSeconds - 0.001);
                    break;
                }
            }
            timeline.setPositionSeconds(seconds);
            timeText.setText(formatTimelineTime(timeline.getVisibleOffsetSeconds(seconds)) + " / "
                    + formatTimelineTime(timeline.getVisibleDurationSeconds()));

            if (videoPreview[0] != null) {
                double offset = 0.0;
                int itemIndex = 0;
                double localSeconds = seconds;
                if (!separateVideoPreviews) {
                    for (; itemIndex < previewVideoDurations.length - 1; itemIndex++) {
                        double next = offset + previewVideoDurations[itemIndex];
                        if (seconds < next) break;
                        offset = next;
                    }
                    localSeconds = Math.max(0.0, seconds - offset);
                } else {
                    itemIndex = 0;
                    localSeconds = Math.min(previewVideoDurations[0], seconds);
                }
                previewVideoOffsetSeconds[0] = offset;
                long localMs = Math.max(0L, Math.round(localSeconds * 1000.0));
                pendingVideoSeekMs[0] = localMs;
                if (itemIndex != previewVideoIndex[0]) {
                    previewVideoIndex[0] = itemIndex;
                    videoPreview[0].setExpectedDurationMs((int) Math.min(Integer.MAX_VALUE,
                            Math.round(previewVideoDurations[itemIndex] * 1000.0)));
                    videoPreview[0].setVideoURI(editorItems.get(itemIndex).uri);
                    videoPreview[0].seekTo((int) Math.min(Integer.MAX_VALUE, localMs));
                    if (playWanted[0]) videoPreview[0].start();
                } else {
                    videoPreview[0].seekTo((int) Math.min(Integer.MAX_VALUE, localMs));
                }
                updatePreviewVisual[0].run();
                int mixMs = (int) Math.min(Integer.MAX_VALUE,
                        Math.round(timeline.getVisibleOffsetSeconds(seconds) * 1000.0));
                int mixDurationMs = (int) Math.min(Integer.MAX_VALUE,
                        Math.round(timeline.getVisibleDurationSeconds() * 1000.0));
                videoPreview[0].setBackgroundTimelinePosition(mixMs, mixDurationMs);
            } else if (gifPreview[0] != null) {
                int milliseconds = (int) Math.min(
                        Math.max(0, gifPreview[0].getDuration() - 1),
                        Math.round(seconds * 1000.0));
                gifPreview[0].seekTo(milliseconds);
            }
        };

        timeline.setOnSeekListener((seconds, finished) -> {
            timelineDragging[0] = !finished;
            seekPreviewTo.accept(seconds);
            if (finished) timelineDragging[0] = false;
        });

        playPauseButton.setOnClickListener(v -> {
            if (videoPreview[0] != null) {
                if (playWanted[0] || videoPreview[0].isPlaying()) {
                    playWanted[0] = false;
                    videoPreview[0].pause();
                    playPauseButton.setText("▶");
                    playPauseButton.setContentDescription("播放");
                    updatePreviewVisual[0].run();
                } else {
                    playWanted[0] = true;
                    videoPreview[0].start();
                    playPauseButton.setText("❚❚");
                    playPauseButton.setContentDescription("暂停");
                }
            } else if (gifPreview[0] != null) {
                if (gifPreview[0].isPlaying()) {
                    gifPreview[0].stop();
                    playPauseButton.setText("▶");
                    playPauseButton.setContentDescription("播放");
                } else {
                    gifPreview[0].start();
                    playPauseButton.setText("❚❚");
                    playPauseButton.setContentDescription("暂停");
                }
            }
        });

        pauseEditorPreview = () -> {
            playWanted[0] = false;
            if (videoPreview[0] != null) videoPreview[0].pause();
            if (gifPreview[0] != null) gifPreview[0].stop();
            playPauseButton.setText("▶");
            playPauseButton.setContentDescription("播放");
        };

        final Runnable[] ticker = new Runnable[1];
        ticker[0] = () -> {
            if (editorClosed[0]) return;
            if (!timelineDragging[0]) {
                double seconds = timeline.getPositionSeconds();
                if (videoPreview[0] != null && previewVideoIndex[0] >= 0) {
                    seconds = previewVideoOffsetSeconds[0]
                            + videoPreview[0].getCurrentPosition() / 1000.0;
                    seconds = Math.max(0.0, Math.min(timelineSeconds, seconds));
                    double skippedTo = seconds;
                    for (AnimationEdits.TimeRange deleted : deletedRanges) {
                        if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {
                            skippedTo = Math.min(timelineSeconds, deleted.endSeconds);
                            break;
                        }
                    }
                    if (skippedTo > seconds + 0.0005) {
                        seekPreviewTo.accept(skippedTo);
                        seconds = skippedTo;
                    } else {
                        timeline.setPositionSeconds(seconds);
                    }
                    int mixMs = (int) Math.min(Integer.MAX_VALUE,
                            Math.round(timeline.getVisibleOffsetSeconds(seconds) * 1000.0));
                    int mixDurationMs = (int) Math.min(Integer.MAX_VALUE,
                            Math.round(timeline.getVisibleDurationSeconds() * 1000.0));
                    videoPreview[0].setBackgroundTimelinePosition(mixMs, mixDurationMs);
                    if (!videoPreview[0].isPlaying()) {
                        playWanted[0] = false;
                        playPauseButton.setText("▶");
                        playPauseButton.setContentDescription("播放");
                    }
                } else if (gifPreview[0] != null) {
                    seconds = gifPreview[0].getCurrentPosition() / 1000.0;
                    double skippedTo = seconds;
                    for (AnimationEdits.TimeRange deleted : deletedRanges) {
                        if (seconds >= deleted.startSeconds && seconds < deleted.endSeconds) {
                            skippedTo = Math.min(timelineSeconds, deleted.endSeconds);
                            break;
                        }
                    }
                    if (skippedTo > seconds + 0.0005) {
                        seekPreviewTo.accept(skippedTo);
                        seconds = skippedTo;
                    } else {
                        timeline.setPositionSeconds(seconds);
                    }
                }
                timeText.setText(formatTimelineTime(timeline.getVisibleOffsetSeconds(seconds)) + " / "
                        + formatTimelineTime(timeline.getVisibleDurationSeconds()));
            }
            editorHandler.postDelayed(ticker[0], 100L);
        };

        final TextView editState = text(
                "播放中也可直接点“分割”，会按点击瞬间的位置落点。",
                11, SECONDARY_TEXT, false);
        editState.setPadding(0, dp(5), 0, dp(2));

        final Button splitButton = createEditorButton("分割", true);
        final Button deleteBetweenButton = createEditorButton("删除片段", false);
        final Button reverseBetweenButton = createEditorButton("倒放片段", false);
        final Button undoButton = createEditorButton("↶ 撤销", false);
        final Button redoButton = createEditorButton("↷ 还原", false);

        LinearLayout actionRow = horizontalRow();
        actionRow.setPadding(0, dp(7), 0, 0);
        addCompactButtons(actionRow, splitButton, deleteBetweenButton, reverseBetweenButton);
        content.addView(actionRow, matchWrap());
        LinearLayout historyRow = horizontalRow();
        historyRow.setPadding(0, dp(5), 0, 0);
        addCompactButtons(historyRow, undoButton, redoButton);
        content.addView(historyRow, matchWrap());
        editState.setVisibility(View.GONE);

        Runnable updateTimelineState = () -> {
            timeline.setSplitPoints(splitPoints[0], splitPoints[1]);
            timeline.setRanges(deletedRanges, reversedRanges);
            timeText.setText(formatTimelineTime(
                    timeline.getVisibleOffsetSeconds(timeline.getPositionSeconds())) + " / "
                    + formatTimelineTime(timeline.getVisibleDurationSeconds()));
            if (videoPreview[0] != null) {
                double source = previewVideoIndex[0] >= 0
                        ? previewVideoOffsetSeconds[0] + videoPreview[0].getCurrentPosition() / 1000.0
                        : timeline.getPositionSeconds();
                videoPreview[0].setBackgroundTimelinePosition(
                        (int) Math.min(Integer.MAX_VALUE, Math.round(
                                timeline.getVisibleOffsetSeconds(source) * 1000.0)),
                        (int) Math.min(Integer.MAX_VALUE, Math.round(
                                timeline.getVisibleDurationSeconds() * 1000.0)));
            }
            boolean hasFirstPoint = !Double.isNaN(splitPoints[0]);
            boolean hasTwoPoints = hasFirstPoint && !Double.isNaN(splitPoints[1]);
            boolean validReverseRange = hasTwoPoints
                    && Math.abs(splitPoints[1] - splitPoints[0]) >= 0.01;
            // Imported clip borders and deleted gaps are persistent edit boundaries.
            // After one new split, the neighboring natural boundary can be used immediately.
            boolean hasNaturalSegments = timeline.getEditingBoundaries().size() > 2;
            boolean canDeleteSegment = hasFirstPoint || hasNaturalSegments;
            deleteBetweenButton.setEnabled(canDeleteSegment);
            reverseBetweenButton.setEnabled(validReverseRange);
            applyEditorButtonStyle(deleteBetweenButton, canDeleteSegment, false);
            applyEditorButtonStyle(reverseBetweenButton, validReverseRange, false);
            boolean canUndo = !undoHistory.isEmpty();
            boolean canRedo = !redoHistory.isEmpty();
            undoButton.setEnabled(canUndo);
            redoButton.setEnabled(canRedo);
            applyEditorButtonStyle(undoButton, canUndo, false);
            applyEditorButtonStyle(redoButton, canRedo, false);

            if (hasFirstPoint && !hasTwoPoints) {
                editState.setText(String.format(Locale.CHINA,
                        hasNaturalSegments
                                ? "切点 %.2f 秒；会优先和最近的空隙边界组成一段，直接删除即可。"
                                : "切点 %.2f 秒；把光标移到要删的一侧后点“删除片段”，或再加一个切点。",
                        splitPoints[0]));
            } else if (hasTwoPoints) {
                editState.setText(String.format(Locale.CHINA,
                        "切点 %.2f / %.2f 秒；删除按当前光标所在分段，倒放仍作用于两切点之间。",
                        Math.min(splitPoints[0], splitPoints[1]),
                        Math.max(splitPoints[0], splitPoints[1])));
            } else if (hasNaturalSegments) {
                editState.setText("空隙是片段边界；再分割一次会自动取最近边界，便于继续微调。");
            } else {
                editState.setText("已删除 " + deletedRanges.size() + " 段 · 已倒放 "
                        + reversedRanges.size() + " 段");
            }
        };

        Runnable pushUndoState = () -> {
            undoHistory.push(new EditorTimelineState(
                    deletedRanges, reversedRanges, splitPoints[0], splitPoints[1]));
            while (undoHistory.size() > 50) undoHistory.removeLast();
            redoHistory.clear();
        };
        updateTimelineState.run();

        splitButton.setOnClickListener(v -> {
            // Capture the real playback position at the instant the user taps Split.
            // Do not pause playback: this makes live splitting behave like a normal video editor.
            double point = timeline.getPositionSeconds();
            if (videoPreview[0] != null && previewVideoIndex[0] >= 0) {
                point = previewVideoOffsetSeconds[0]
                        + Math.max(0, videoPreview[0].getCurrentPosition()) / 1000.0;
            } else if (gifPreview[0] != null) {
                point = Math.max(0, gifPreview[0].getCurrentPosition()) / 1000.0;
            }
            point = Math.max(0.0, Math.min(timelineSeconds, point));
            timeline.setPositionSeconds(point);
            timeText.setText(formatTimelineTime(timeline.getVisibleOffsetSeconds(point)) + " / "
                    + formatTimelineTime(timeline.getVisibleDurationSeconds()));

            pushUndoState.run();
            if (Double.isNaN(splitPoints[0]) || !Double.isNaN(splitPoints[1])) {
                splitPoints[0] = point;
                splitPoints[1] = Double.NaN;
            } else {
                splitPoints[1] = point;
            }
            updateTimelineState.run();
        });

        deleteBetweenButton.setOnClickListener(v -> {
            // Natural clip borders and previous deletion gaps act like permanent split points.
            // A single new split is therefore enough to shave a few more seconds from either side.
            double point = timeline.getPositionSeconds();
            if (videoPreview[0] != null && previewVideoIndex[0] >= 0) {
                point = previewVideoOffsetSeconds[0]
                        + Math.max(0, videoPreview[0].getCurrentPosition()) / 1000.0;
            } else if (gifPreview[0] != null) {
                point = Math.max(0, gifPreview[0].getCurrentPosition()) / 1000.0;
            }
            point = Math.max(0.0, Math.min(timelineSeconds, point));

            List<Double> boundaries = new ArrayList<>(timeline.getEditingBoundaries());
            if (!Double.isNaN(splitPoints[0])) {
                boundaries.add(Math.max(0.0, Math.min(timelineSeconds, splitPoints[0])));
            }
            if (!Double.isNaN(splitPoints[1])) {
                boundaries.add(Math.max(0.0, Math.min(timelineSeconds, splitPoints[1])));
            }
            Collections.sort(boundaries);

            // Remove accidental duplicate cut positions so a zero-length segment is never chosen.
            List<Double> unique = new ArrayList<>();
            for (double boundary : boundaries) {
                if (unique.isEmpty() || Math.abs(boundary - unique.get(unique.size() - 1)) >= 0.01) {
                    unique.add(boundary);
                }
            }
            if (unique.size() < 2) return;

            double startPoint = unique.get(0);
            double endPoint = unique.get(1);
            boolean picked = false;

            // With one new split inside an already segmented timeline, pressing Delete right away
            // trims from that split to the nearest persistent clip edge. This matches the common
            // gallery/editor gesture: an old cut supplies one edge, so the user only marks once.
            if (!Double.isNaN(splitPoints[0]) && Double.isNaN(splitPoints[1])
                    && Math.abs(point - splitPoints[0]) < 0.03) {
                List<Double> persistent = timeline.getEditingBoundaries();
                if (persistent.size() > 2) {
                    double split = splitPoints[0];
                    double leftBoundary = Double.NaN;
                    double rightBoundary = Double.NaN;
                    for (double boundary : persistent) {
                        if (boundary < split - 0.01) leftBoundary = boundary;
                        else if (boundary > split + 0.01) {
                            rightBoundary = boundary;
                            break;
                        }
                    }
                    double leftDistance = Double.isNaN(leftBoundary)
                            ? Double.POSITIVE_INFINITY : split - leftBoundary;
                    double rightDistance = Double.isNaN(rightBoundary)
                            ? Double.POSITIVE_INFINITY : rightBoundary - split;
                    if (leftDistance < Double.POSITIVE_INFINITY
                            || rightDistance < Double.POSITIVE_INFINITY) {
                        if (leftDistance <= rightDistance) {
                            startPoint = leftBoundary;
                            endPoint = split;
                        } else {
                            startPoint = split;
                            endPoint = rightBoundary;
                        }
                        picked = endPoint - startPoint >= 0.01;
                    }
                }
            }

            if (!picked) {
                for (int i = 0; i + 1 < unique.size(); i++) {
                    double candidateStart = unique.get(i);
                    double candidateEnd = unique.get(i + 1);
                    boolean last = i + 2 == unique.size();
                    if ((point >= candidateStart && point < candidateEnd)
                            || (last && point <= candidateEnd)) {
                        startPoint = candidateStart;
                        endPoint = candidateEnd;
                        break;
                    }
                }
            }
            if (endPoint - startPoint < 0.01) return;

            for (AnimationEdits.TimeRange deleted : deletedRanges) {
                if (point >= deleted.startSeconds && point < deleted.endSeconds) {
                    toast("当前光标所在片段已经删除");
                    return;
                }
            }

            pushUndoState.run();
            deletedRanges.add(new AnimationEdits.TimeRange(startPoint, endPoint));
            splitPoints[0] = Double.NaN;
            splitPoints[1] = Double.NaN;
            double resumePoint = endPoint < timelineSeconds - 0.001
                    ? endPoint : Math.max(0.0, startPoint - 0.001);
            seekPreviewTo.accept(Math.min(timelineSeconds, resumePoint));
            updateTimelineState.run();
            updatePreviewVisual[0].run();
        });

        reverseBetweenButton.setOnClickListener(v -> {
            if (Double.isNaN(splitPoints[0]) || Double.isNaN(splitPoints[1])) return;
            double startPoint = Math.min(splitPoints[0], splitPoints[1]);
            double endPoint = Math.max(splitPoints[0], splitPoints[1]);
            if (endPoint - startPoint < 0.01) return;
            pushUndoState.run();
            reversedRanges.add(new AnimationEdits.TimeRange(startPoint, endPoint));
            splitPoints[0] = Double.NaN;
            splitPoints[1] = Double.NaN;
            updateTimelineState.run();
            updatePreviewVisual[0].run();
        });

        undoButton.setOnClickListener(v -> {
            if (undoHistory.isEmpty()) return;
            redoHistory.push(new EditorTimelineState(
                    deletedRanges, reversedRanges, splitPoints[0], splitPoints[1]));
            EditorTimelineState state = undoHistory.pop();
            deletedRanges.clear();
            deletedRanges.addAll(state.deletedRanges);
            reversedRanges.clear();
            reversedRanges.addAll(state.reversedRanges);
            splitPoints[0] = state.splitPoint1;
            splitPoints[1] = state.splitPoint2;
            updateTimelineState.run();
            updatePreviewVisual[0].run();
        });

        redoButton.setOnClickListener(v -> {
            if (redoHistory.isEmpty()) return;
            undoHistory.push(new EditorTimelineState(
                    deletedRanges, reversedRanges, splitPoints[0], splitPoints[1]));
            EditorTimelineState state = redoHistory.pop();
            deletedRanges.clear();
            deletedRanges.addAll(state.deletedRanges);
            reversedRanges.clear();
            reversedRanges.addAll(state.reversedRanges);
            splitPoints[0] = state.splitPoint1;
            splitPoints[1] = state.splitPoint2;
            updateTimelineState.run();
            updatePreviewVisual[0].run();
        });

        boolean timedSource = hasTimedSourceSelected();
        final boolean finalTimedSource = timedSource;
        final EditText startEdit = numberField("开始秒数", formatEditorNumber(
                current.trimStartSeconds), true);
        final EditText durationEdit = numberField("保留时长；0=全部", formatEditorNumber(
                current.trimDurationSeconds), true);
        if (timedSource) {
            addLabelWithTop(content, editorItems.size() > 1
                    ? "精确截取（每个视频，可选）" : "精确截取（可选）", PRIMARY_TEXT);
            LinearLayout timeRow = horizontalRow();
            addTwoFields(timeRow, startEdit, durationEdit);
            content.addView(timeRow, matchWrap());
        }

        final double[] selectedSpeed = {Math.max(0.25, Math.min(10.0, current.speed))};
        final TextView speedValue = addLabelWithTop(content,
                "速度 · " + formatSpeedMultiplier(selectedSpeed[0]), PRIMARY_TEXT);
        final SeekBar speedSeek = new SeekBar(this);
        speedSeek.setMin(25);
        speedSeek.setMax(1000);
        speedSeek.setProgress((int) Math.round(selectedSpeed[0] * 100.0));
        content.addView(speedSeek, matchWrap());
        final double[] speedAnchors = {0.5, 1.0, 1.5, 2.0, 4.0, 10.0};
        final Runnable updateSpeedValue = () -> speedValue.setText(
                "速度 · " + formatSpeedMultiplier(selectedSpeed[0]));
        speedSeek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                selectedSpeed[0] = Math.max(0.25, Math.min(10.0, progress / 100.0));
                updateSpeedValue.run();
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) { }
            @Override public void onStopTrackingTouch(SeekBar seekBar) {
                double nearest = selectedSpeed[0];
                double distance = Double.MAX_VALUE;
                for (double anchor : speedAnchors) {
                    double currentDistance = Math.abs(selectedSpeed[0] - anchor);
                    if (currentDistance < distance) {
                        nearest = anchor;
                        distance = currentDistance;
                    }
                }
                // Close values magnetically snap to common speeds, while the rest stay fully free.
                if (distance <= 0.04) {
                    selectedSpeed[0] = nearest;
                    speedSeek.setProgress((int) Math.round(nearest * 100.0));
                    speedSeek.performHapticFeedback(android.view.HapticFeedbackConstants.CLOCK_TICK);
                }
                updateSpeedValue.run();
            }
        });
        LinearLayout speedAnchorRow = horizontalRow();
        Button speed05 = createEditorButton("0.5×", false);
        Button speed10 = createEditorButton("1×", false);
        Button speed15 = createEditorButton("1.5×", false);
        Button speed20 = createEditorButton("2×", false);
        Button speed40 = createEditorButton("4×", false);
        Button speed100 = createEditorButton("10×", false);
        Button[] speedButtons = {speed05, speed10, speed15, speed20, speed40, speed100};
        for (Button button : speedButtons) button.setTextSize(12);
        speed05.setOnClickListener(v -> speedSeek.setProgress(50));
        speed10.setOnClickListener(v -> speedSeek.setProgress(100));
        speed15.setOnClickListener(v -> speedSeek.setProgress(150));
        speed20.setOnClickListener(v -> speedSeek.setProgress(200));
        speed40.setOnClickListener(v -> speedSeek.setProgress(400));
        speed100.setOnClickListener(v -> speedSeek.setProgress(1000));
        addCompactButtons(speedAnchorRow, speed05, speed10, speed15, speed20, speed40, speed100);
        content.addView(speedAnchorRow, matchWrap());

        addLabelWithTop(content, "画面", PRIMARY_TEXT);
        final Spinner cropSpinner = createSpinner(EDIT_CROP_OPTIONS);
        cropSpinner.setSelection(current.cropMode);
        content.addView(cropSpinner, matchWrap());
        final Spinner rotationSpinner = createSpinner(EDIT_ROTATION_OPTIONS);
        rotationSpinner.setSelection((current.rotationDegrees / 90) & 3);
        LinearLayout.LayoutParams rotationParams = matchWrap();
        rotationParams.topMargin = dp(4);
        content.addView(rotationSpinner, rotationParams);

        final CheckBox flipHorizontal = new CheckBox(this);
        flipHorizontal.setText("水平镜像");
        flipHorizontal.setChecked(current.flipHorizontal);
        final CheckBox flipVertical = new CheckBox(this);
        flipVertical.setText("垂直镜像");
        flipVertical.setChecked(current.flipVertical);
        LinearLayout flipRow = horizontalRow();
        flipRow.addView(flipHorizontal, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        flipRow.addView(flipVertical, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        content.addView(flipRow, matchWrap());

        addLabelWithTop(content, "基础调色", PRIMARY_TEXT);
        final TextView brightnessText = text("", 12, SECONDARY_TEXT, false);
        final SeekBar brightnessSeek = new SeekBar(this);
        brightnessSeek.setMax(100);
        brightnessSeek.setProgress(current.brightness + 50);
        final TextView contrastText = text("", 12, SECONDARY_TEXT, false);
        final SeekBar contrastSeek = new SeekBar(this);
        contrastSeek.setMax(100);
        contrastSeek.setProgress(current.contrast - 50);
        final TextView saturationText = text("", 12, SECONDARY_TEXT, false);
        final SeekBar saturationSeek = new SeekBar(this);
        saturationSeek.setMax(200);
        saturationSeek.setProgress(current.saturation);

        Runnable updateColorPreview = () -> {
            previewBrightness[0] = brightnessSeek.getProgress() - 50;
            previewContrast[0] = contrastSeek.getProgress() + 50;
            previewSaturation[0] = saturationSeek.getProgress();
            brightnessText.setText("亮度 " + previewBrightness[0]);
            contrastText.setText("对比度 " + previewContrast[0] + "%");
            saturationText.setText("饱和度 " + previewSaturation[0] + "%");
            updatePreviewVisual[0].run();
        };
        brightnessSeek.setOnSeekBarChangeListener(seekListener(updateColorPreview));
        contrastSeek.setOnSeekBarChangeListener(seekListener(updateColorPreview));
        saturationSeek.setOnSeekBarChangeListener(seekListener(updateColorPreview));

        AdapterView.OnItemSelectedListener visualSpinnerListener =
                new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> parent, View view,
                                                 int position, long id) {
                previewCropMode[0] = cropSpinner.getSelectedItemPosition();
                previewRotation[0] = rotationSpinner.getSelectedItemPosition() * 90;
                updatePreviewVisual[0].run();
            }
            @Override public void onNothingSelected(AdapterView<?> parent) { }
        };
        cropSpinner.setOnItemSelectedListener(visualSpinnerListener);
        rotationSpinner.setOnItemSelectedListener(visualSpinnerListener);
        flipHorizontal.setOnCheckedChangeListener((button, checked) -> {
            previewFlipHorizontal[0] = checked;
            updatePreviewVisual[0].run();
        });
        flipVertical.setOnCheckedChangeListener((button, checked) -> {
            previewFlipVertical[0] = checked;
            updatePreviewVisual[0].run();
        });

        updateColorPreview.run();
        content.addView(brightnessText);
        content.addView(brightnessSeek, matchWrap());
        content.addView(contrastText);
        content.addView(contrastSeek, matchWrap());
        content.addView(saturationText);
        content.addView(saturationSeek, matchWrap());

        addLabelWithTop(content, "直接导出", PRIMARY_TEXT);
        final Spinner editorOutput = createSpinner(new String[]{
                "MP4 · H.264（兼容优先）", "MP4 · H.265", "MP4 · AV1（需设备支持）"});
        int existingFormat = selectedOutputFormat();
        editorOutput.setSelection(existingFormat >= 4 && existingFormat <= 6 ? existingFormat - 4 : 0);
        content.addView(editorOutput, matchWrap());
        Button resetEditor = createButton("重置剪辑", false);
        content.addView(resetEditor, matchWrap());
        Runnable saveEdits = () -> {
            animationEdits = new AnimationEdits(
                    finalTimedSource ? parseDouble(startEdit.getText().toString(), 0) : 0,
                    finalTimedSource ? parseDouble(durationEdit.getText().toString(), 0) : 0,
                    selectedSpeed[0],
                    cropSpinner.getSelectedItemPosition(), rotationSpinner.getSelectedItemPosition() * 90,
                    flipHorizontal.isChecked(), flipVertical.isChecked(),
                    brightnessSeek.getProgress() - 50, contrastSeek.getProgress() + 50,
                    saturationSeek.getProgress(), deletedRanges, reversedRanges);
            saveEditorColorDefaults(animationEdits);
            editsCommitted[0] = true;
            if (afterSave != null) afterSave.run();
            updateControlStates();
        };
        AlertDialog dialog = new AlertDialog.Builder(this)
                .setTitle("视频 / GIF 剪辑")
                .setView(scroll)
                .setPositiveButton("导出 MP4", null)
                .setNeutralButton("保存剪辑", null)
                .setNegativeButton("取消", null)
                .create();
        resetEditor.setOnClickListener(v -> {
            startEdit.setText("0"); durationEdit.setText("0");
            selectedSpeed[0] = 1.0;
            speedSeek.setProgress(100);
            updateSpeedValue.run();
            cropSpinner.setSelection(0); rotationSpinner.setSelection(0);
            flipHorizontal.setChecked(false); flipVertical.setChecked(false);
            brightnessSeek.setProgress(DEFAULT_EDITOR_BRIGHTNESS + 50);
            contrastSeek.setProgress(DEFAULT_EDITOR_CONTRAST - 50);
            saturationSeek.setProgress(DEFAULT_EDITOR_SATURATION);
            deletedRanges.clear(); reversedRanges.clear();
            undoHistory.clear(); redoHistory.clear();
            splitPoints[0] = Double.NaN; splitPoints[1] = Double.NaN;
            updateTimelineState.run(); updateColorPreview.run();
            toast("已重置画面与时间轴；声音设置保留");
        });
        dialog.setOnDismissListener(ignored -> {
            editorClosed[0] = true;
            if (activeAudioDialog != null) activeAudioDialog.dismiss();
            activeEditorDialog = null;
            pauseEditorPreview = null;
            refreshEditorAudio = null;
            if (!editsCommitted[0]) {
                backgroundMusic = savedMusic;
                originalVolume = savedOriginalVolume; musicVolume = savedMusicVolume;
                musicLoop = savedMusicLoop; musicStartSeconds = savedMusicStart;
                audioFadeSeconds = savedAudioFade;
            }
            editorHandler.removeCallbacksAndMessages(null);
            if (videoPreview[0] != null) {
                try { videoPreview[0].stopPlayback(); } catch (Exception ignoredError) { }
            }
            if (gifPreview[0] != null) {
                if (gifPreviewView[0] != null) gifPreviewView[0].setImageDrawable(null);
                try { gifPreview[0].stop(); } catch (Exception ignoredError) { }
                try { gifPreview[0].recycle(); } catch (Exception ignoredError) { }
            }
        });
        dialog.show();
        activeEditorDialog = dialog;
        dialog.getButton(AlertDialog.BUTTON_NEUTRAL).setOnClickListener(v -> {
            saveEdits.run();
            dialog.dismiss();
        });
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            if (busy) return;
            saveEdits.run();
            int outputFormat = editorOutput.getSelectedItemPosition() + 4;
            if (pauseEditorPreview != null) pauseEditorPreview.run();
            if (videoPreview[0] != null) videoPreview[0].stopPlayback();
            dialog.dismiss();
            // Dismiss callbacks finish before export captures settings and starts its codecs.
            selectedRecycler.post(() -> {
                if (isFinishing() || isDestroyed() || busy) return;
                setSelectedOutputFormat(outputFormat);
                updateControlStates();
                beginConversionInternal(BatchMode.SINGLE, editorItems, outputFormat);
            });
        });
        seekPreviewTo.accept(0.0);
        editorHandler.post(ticker[0]);
    }

    private double estimateEditTimelineSeconds(List<SelectedItem> editorItems) {
        if (editorItems.isEmpty()) return 1.0;
        double totalSeconds = 0.0;
        for (SelectedItem item : editorItems) {
            double itemSeconds = 0.0;
            if (item.isVideo()) {
                itemSeconds = videoDurationSeconds(item);
            } else if (item.sourceFormat == SourceFormat.GIF) {
                try {
                    itemSeconds = Math.max(1, new pl.droidsonroids.gif.GifAnimationMetaData(
                            getContentResolver(), item.uri).getDuration()) / 1000.0;
                } catch (Exception ignored) { }
            }
            totalSeconds += itemSeconds;
        }
        if (totalSeconds <= 0.0) {
            totalSeconds = editorItems.size() / (double) Math.max(1, selectedFps());
        }
        return Math.max(0.1, Math.min(86_400.0, totalSeconds));
    }

    private double videoDurationSeconds(SelectedItem item) {
        if (item == null || !item.isVideo()) return 0.0;
        MediaMetadataRetriever retriever = new MediaMetadataRetriever();
        try {
            retriever.setDataSource(this, item.uri);
            String duration = retriever.extractMetadata(
                    MediaMetadataRetriever.METADATA_KEY_DURATION);
            return Math.max(0L, parseLong(duration, 0L)) / 1000.0;
        } catch (Throwable ignored) {
            // The conversion preflight reports a precise error if the system decoder cannot
            // read this item; leaving it at zero keeps the editor usable for the other clips.
            return 0.0;
        } finally {
            try { retriever.release(); } catch (Throwable ignored) { }
        }
    }

    private static String formatSpeedMultiplier(double speed) {
        String value = String.format(Locale.CHINA, "%.2f", speed);
        while (value.endsWith("0")) value = value.substring(0, value.length() - 1);
        if (value.endsWith(".")) value = value.substring(0, value.length() - 1);
        return value + "×";
    }

    private static int nearestSpeedIndex(double speed) {
        int best = 0;
        double bestDistance = Double.MAX_VALUE;
        for (int i = 0; i < EDIT_SPEED_VALUES.length; i++) {
            double distance = Math.abs(EDIT_SPEED_VALUES[i] - speed);
            if (distance < bestDistance) {
                best = i;
                bestDistance = distance;
            }
        }
        return best;
    }

    private static String formatEditorNumber(double value) {
        if (Math.abs(value - Math.rint(value)) < 0.0001) {
            return String.format(Locale.CHINA, "%.0f", value);
        }
        return String.format(Locale.CHINA, "%.2f", value);
    }

    private void beginConversionInternal(BatchMode batchMode) {
        ActionState action = evaluateActionState();
        if (!action.enabled || busy) return;
        beginConversionInternal(batchMode, selectedItems, selectedOutputFormat());
    }

    private void beginConversionInternal(BatchMode batchMode, List<SelectedItem> inputs,
                                         final int selectedFormat) {
        if (busy || inputs.isEmpty()) return;
        final int quality = qualitySeek.getProgress();
        final int fps = selectedFps();
        final int frameLimit = selectedFrameLimit();
        final int bitrate = selectedBitrate();
        final int loops = selectedLoops();
        final int videoLoops = selectedVideoLoops();
        final int reverseLoop = selectedReverseLoop();
        final int resolutionPosition = resolutionSpinner.getSelectedItemPosition();
        final int customWidth = clamp(parseInt(customWidthEdit.getText().toString(), 1280), 16, 8192);
        final int customHeight = clamp(parseInt(customHeightEdit.getText().toString(), 720), 16, 8192);
        final boolean keepOriginalResolution = resolutionPosition <= 1;
        final boolean qualityWasTouched = qualityTouched && resolutionPosition != 0;
        final List<SelectedItem> items = new ArrayList<>(inputs);
        final boolean separateVideoGifs = selectedFormat == 3
                && items.size() > 1
                && hasOnlyVideos(items)
                && videoGifOutputSpinner.getSelectedItemPosition() == 1;
        runningSettings = new ConversionSettings(
                resolutionPosition, customWidth, customHeight,
                animationEdits == null ? freshAnimationEdits() : animationEdits,
                gifReplaySpinner.getSelectedItemPosition() == 1 ? -1 : 0);

        exportAudioSettings = new AudioPipeline.Settings(backgroundMusic, originalVolume, musicVolume,
                musicLoop, musicStartSeconds, audioFadeSeconds);
        cancelRequested = false;
        setBusy(true);
        recommendationGeneration++;
        recommendationHandler.removeCallbacksAndMessages(null);
        if (recommendationTask != null) recommendationTask.cancel(true);
        thumbnailCache.trimToSize(thumbnailCache.maxSize() / 4);
        updateProgress(0, "正在准备……");

        currentTask = executor.submit(() -> {
            taskRunning = true;
            try {
                checkCancelled();
                ensureCacheCapacity();
                ConversionResult singleResult = null;
                BatchConversionResult batchResult = null;
                if (selectedFormat == 9 || selectedFormat == 10 || selectedFormat == 27) {
                    singleResult = videoToAudio(items.get(0), selectedFormat);
                } else if (selectedFormat == 11) {
                    if (items.get(0).sourceFormat == SourceFormat.PDF) {
                        File merged = cacheFile(".pdf");
                        List<Uri> uris = new ArrayList<>();
                        for (SelectedItem item : items) uris.add(item.uri);
                        DocumentKit.mergePdf(this, uris, merged, this::checkCancelled);
                        singleResult = new ConversionResult(merged,"application/pdf","merged.pdf");
                    } else singleResult = imagesToPdf(items, quality, qualityWasTouched);
                } else if (selectedFormat == 12) {
                    if (items.size() == 1) {
                        singleResult = imageToIco(items.get(0));
                    } else if (batchMode == BatchMode.ZIP) {
                        singleResult = imagesToIcoZip(items);
                    } else {
                        batchResult = imagesToIcoBatch(items);
                    }
                } else if (isTextOutputFormat(selectedFormat)) {
                    if (items.size() == 1) {
                        singleResult = convertTextDocument(items.get(0), selectedFormat,
                                quality, qualityWasTouched);
                    } else if (batchMode == BatchMode.ZIP) {
                        singleResult = textBatchToZip(items, selectedFormat,
                                quality, qualityWasTouched);
                    } else {
                        batchResult = new BatchConversionResult(
                                textBatchFiles(items, selectedFormat, quality, qualityWasTouched));
                    }
                } else if (isPdfToStaticImagesMode(selectedFormat, items)) {
                    List<PendingBatchFile> pages = renderPdfPages(
                            items.get(0), selectedFormat, quality, qualityWasTouched,
                            resolutionPosition, customWidth, customHeight);
                    try {
                        if (batchMode == BatchMode.ZIP) {
                            singleResult = zipPendingFiles(pages,
                                    "converted_" + outputSpec(selectedFormat).shortName
                                            .toLowerCase(Locale.ROOT)
                                            + "_" + pages.size() + "_files.zip");
                        } else if (pages.size() == 1) {
                            PendingBatchFile page = pages.get(0);
                            singleResult = new ConversionResult(
                                    page.file, page.mime, page.fileName);
                        } else {
                            batchResult = new BatchConversionResult(pages);
                        }
                    } catch (Throwable error) {
                        deleteBatchFiles(pages);
                        throw error;
                    }
                } else if (selectedFormat >= 4 && selectedFormat <= 6) {
                    SelectedItem item = items.get(0);
                    if (item.isVideo()) {
                        singleResult = videosToMp4(items, fps, frameLimit, bitrate, loops, selectedFormat);
                    } else {
                        singleResult = gifToMp4(item.uri, item.name, fps, frameLimit,
                                bitrate, loops, selectedFormat);
                        singleResult = attachVideoAudio(singleResult, Collections.emptyList(), loops);
                    }
                } else if (selectedFormat == 3) {
                    SelectedItem first = items.get(0);
                    if (first.isVideo()) {
                        if (separateVideoGifs) {
                            batchResult = videosToGifBatch(items, fps, frameLimit,
                                    videoLoops, reverseLoop);
                        } else {
                            singleResult = videosToGif(items, fps, frameLimit,
                                    videoLoops, reverseLoop);
                        }
                    } else if (items.size() == 1 && first.sourceFormat == SourceFormat.GIF) {
                        singleResult = gifToGif(first.uri, first.name, fps, frameLimit, videoLoops, reverseLoop);
                    } else {
                        singleResult = imagesToGif(items, fps, frameLimit);
                    }
                } else if (items.size() == 1) {
                    singleResult = convertStaticImage(
                            items.get(0), selectedFormat, quality, qualityWasTouched);
                } else if (batchMode == BatchMode.ZIP) {
                    singleResult = convertStaticBatch(items, selectedFormat, quality,
                            keepOriginalResolution, qualityWasTouched);
                } else {
                    batchResult = convertStaticBatchFiles(items, selectedFormat, quality,
                            keepOriginalResolution, qualityWasTouched);
                }
                checkCancelled();
                activeWorkFile = null;
                final ConversionResult completedSingle = singleResult;
                final BatchConversionResult completedBatch = batchResult;
                runOnUiThread(() -> {
                    if (cancelRequested) {
                        if (completedSingle != null && completedSingle.file.exists()) {
                            completedSingle.file.delete();
                        }
                        if (completedBatch != null) deleteBatchFiles(completedBatch.files);
                        finishCancelledUi();
                        return;
                    }
                    updateProgress(1000, "转换完成");
                    if (completedBatch != null) {
                        pendingBatchFiles = new ArrayList<>(completedBatch.files);
                        statusText.setText("转换完成，请选择保存文件夹。");
                        launchSaveFolderPicker();
                    } else if (completedSingle != null) {
                        pendingOutput = completedSingle.file;
                        pendingFileName = completedSingle.fileName;
                        statusText.setText("转换完成，请选择保存位置。");
                        launchSavePicker(completedSingle);
                    } else {
                        cleanupPending();
                        setBusy(false);
                        statusText.setText("转换失败：没有生成输出文件。");
                    }
                });
            } catch (Throwable error) {
                boolean cancelled = cancelRequested || Thread.currentThread().isInterrupted()
                        || error instanceof CancelledException;
                deleteActiveWorkFile();
                runOnUiThread(() -> {
                    if (cancelled) {
                        finishCancelledUi();
                    } else {
                        cleanupPending();
                        setBusy(false);
                        String message = safeMessage(error);
                        statusText.setText("转换失败：" + message);
                        toast("转换失败");
                    }
                });
            } finally {
                taskRunning = false;
                currentTask = null;
            }
        });
    }

    private boolean isStaticOutputFormat(int format) {
        return format == 0 || format == 1 || format == 2 || format == 7 || format == 8 || (format >= 29 && format <= 34);
    }

    private ConversionResult videoToAudio(SelectedItem item, int format) throws Exception {
        if (item == null || (!item.isVideo() && item.sourceFormat != SourceFormat.AUDIO)) throw new IOException("请选择音频或视频文件");
        OutputSpec spec = outputSpec(format);
        File output = cacheFile(spec.extension);
        updateProgress(0, "正在准备音频……");
        if (format == 9) {
            AudioConverter.videoToMp3(this,item.uri,output,this::isCancellationRequested,this::updateProgress);
        } else if (format == 10 && AudioPipeline.isAac(this,item.uri)) {
            AudioConverter.videoToM4a(this,item.uri,output,this::isCancellationRequested,this::updateProgress);
        } else {
            AudioPipeline.convert(this,item.uri,output,format == 27,this::checkCancelled,this::updateProgress);
        }
        checkCancelled();
        if (output.length() <= 0) throw new IOException("音频输出为空");
        return new ConversionResult(output,spec.mime,safeBaseName(item.name)+spec.extension);
    }

    private ConversionResult videosToMp4(List<SelectedItem> items,int fps,int frameLimit,int bitrate,int loops,int format) throws Exception {
        AnimationEdits edits=currentAnimationEdits();
        List<VideoFrameDecoder.Info> infos=new ArrayList<>();
        List<Long> starts=new ArrayList<>(),ends=new ArrayList<>();
        for(SelectedItem item:items) {
            checkCancelled();
            VideoFrameDecoder.Info info=VideoFrameDecoder.probe(this,item.uri);
            long start=Math.min(Math.max(0,Math.round(edits.trimStartSeconds*1e6)),Math.max(0,info.durationUs-1));
            long end=edits.trimDurationSeconds<=0?info.durationUs:Math.min(info.durationUs,start+Math.round(edits.trimDurationSeconds*1e6));
            if(end<=start)throw new IOException("视频截取范围为空");
            infos.add(info);starts.add(start);ends.add(end);
        }
        VideoTimeline timeline=buildVideoTimeline(items,infos,starts,ends,edits);
        List<AudioPipeline.Segment> segments=new ArrayList<>();
        for(int i=0;i<timeline.items.size();i++)segments.add(new AudioPipeline.Segment(
                timeline.items.get(i).uri,timeline.startsUs.get(i),timeline.endsUs.get(i),timeline.reversed.get(i),edits.speed));
        if(segments.isEmpty())throw new IOException("删除后没有保留片段");
        int[] edited=FrameEditor.editedSize(infos.get(0).orientedWidth(),infos.get(0).orientedHeight(),edits);
        int[] bounds=selectedBounds(edited[0],edited[1],false);
        int[] size=fitSize(edited[0],edited[1],bounds[0],bounds[1],true);
        VideoCodecSpec codec=videoCodecSpec(format);
        File video=cacheFile(".mp4");
        VideoExporter.export(this,segments,edits,video,size[0],size[1],fps,frameLimit,loops,bitrate,
                codec.mime,codec.label,this::checkCancelled,(v,m)->updateProgress(v*7/10,m));
        return attachVideoAudio(new ConversionResult(video,"video/mp4",safeBaseName(items.get(0).name)+"_edited.mp4"),segments,loops);
    }

    private ConversionResult attachVideoAudio(ConversionResult video,List<AudioPipeline.Segment> segments,int loops) throws Exception {
        File result=AudioPipeline.attach(this,video.file,segments,loops,exportAudioSettings,
                this::checkCancelled,(v,m)->updateProgress(700+v*3/10,m));
        if(result!=video.file){video.file.delete();activeWorkFile=result;}
        return new ConversionResult(result,"video/mp4",video.fileName);
    }

    private void showAudioSettings() {
        if (busy || activeEditorDialog == null || activeAudioDialog != null) return;
        LinearLayout content=new LinearLayout(this);content.setOrientation(LinearLayout.VERTICAL);content.setPadding(dp(20),dp(8),dp(20),dp(12));
        TextView originalLabel=text("原声音量："+Math.round(originalVolume*100)+"%",14,PRIMARY_TEXT,false);content.addView(originalLabel);
        SeekBar original=new SeekBar(this);original.setMax(200);original.setProgress(Math.round(originalVolume*100));content.addView(original);
        TextView musicLabel=text("音乐音量："+Math.round(musicVolume*100)+"%",14,PRIMARY_TEXT,false);content.addView(musicLabel);
        SeekBar music=new SeekBar(this);music.setMax(200);music.setProgress(Math.round(musicVolume*100));content.addView(music);
        original.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){public void onProgressChanged(SeekBar b,int v,boolean u){originalLabel.setText("原声音量："+v+"%");}public void onStartTrackingTouch(SeekBar b){}public void onStopTrackingTouch(SeekBar b){}});
        music.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){public void onProgressChanged(SeekBar b,int v,boolean u){musicLabel.setText("音乐音量："+v+"%");}public void onStartTrackingTouch(SeekBar b){}public void onStopTrackingTouch(SeekBar b){}});
        android.widget.CheckBox loop=new android.widget.CheckBox(this);loop.setText("音乐不足时循环播放");loop.setChecked(musicLoop);content.addView(loop);
        EditText start=new EditText(this);start.setHint("音乐起点（秒）");start.setInputType(android.text.InputType.TYPE_CLASS_NUMBER|android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);start.setText(String.valueOf(musicStartSeconds));content.addView(text("音乐起点（秒）",13,SECONDARY_TEXT,false));content.addView(start);
        EditText fade=new EditText(this);fade.setHint("淡入淡出时长（0–10 秒）");fade.setInputType(android.text.InputType.TYPE_CLASS_NUMBER|android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);fade.setText(String.valueOf(audioFadeSeconds));content.addView(text("首尾淡入淡出（秒，0 为关闭）",13,SECONDARY_TEXT,false));content.addView(fade);
        TextView chosen=text(backgroundMusic==null?"未选择背景音乐":"已选择："+queryDisplayName(backgroundMusic),13,SECONDARY_TEXT,false);content.addView(chosen);
        final Uri[] draftMusic={backgroundMusic};
        Button remove=new Button(this);remove.setText("移除背景音乐");remove.setOnClickListener(v->{draftMusic[0]=null;chosen.setText("未选择背景音乐");});content.addView(remove);
        Runnable save=()->{backgroundMusic=draftMusic[0];originalVolume=original.getProgress()/100f;musicVolume=music.getProgress()/100f;musicLoop=loop.isChecked();musicStartSeconds=Math.max(0,Math.min(86400,parseDouble(start.getText().toString(),0)));audioFadeSeconds=Math.max(0,Math.min(10,parseDouble(fade.getText().toString(),0)));};
        ScrollView scroll=new ScrollView(this);scroll.addView(content);
        AlertDialog soundDialog = new AlertDialog.Builder(this).setTitle("剪辑 · 声音设置").setView(scroll)
                .setPositiveButton("保存",(d,w)->save.run())
                .setNeutralButton("选择音乐",(d,w)->{save.run();Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("audio/*");intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);startActivityForResult(intent,REQUEST_MUSIC);})
                .setNegativeButton("关闭",null).create();
        activeAudioDialog = soundDialog;
        soundDialog.setOnDismissListener(d -> {
            activeAudioDialog = null;
            if (refreshEditorAudio != null) refreshEditorAudio.run();
        });
        soundDialog.show();
    }

    private ConversionResult convertStaticImage(
            SelectedItem item, int format, int quality,
            boolean qualityWasTouched) throws Exception {
        updateProgress(60, "正在读取图片……");
        checkCancelled();
        int[] bounds = selectedBounds(0, 0, false);
        Bitmap bitmap = decodeBitmap(item.uri, bounds[0], bounds[1], 80_000_000L);
        checkCancelled();
        if (bitmap == null) throw new IOException("无法解码图片");
        ensureCacheCapacity(estimatedStaticOutputBytes(
                format, bitmap.getWidth(), bitmap.getHeight()));

        OutputSpec spec = outputSpec(format);
        File output = cacheFile(spec.extension);
        try (OutputStream out = new BufferedOutputStream(
                new FileOutputStream(output), 256 * 1024)) {
            int effectiveQuality = resolvedImageQuality(
                    item, bitmap, format, quality, qualityWasTouched);
            boolean smartLossy = !qualityWasTouched
                    && isSmartResolution() && (format == 0 || format == 7);
            updateProgress(180, smartLossy
                    ? "实际参数：" + bitmap.getWidth() + "×" + bitmap.getHeight() + " · 智能质量 " + effectiveQuality + "/100，正在编码……"
                    : "正在编码图片……");
            encodeBitmap(bitmap, format, effectiveQuality, out);
        } finally {
            bitmap.recycle();
        }
        checkCancelled();
        if (output.length() == 0) {
            output.delete();
            throw new IOException("编码失败");
        }
        updateProgress(1000, "图片转换完成");
        return new ConversionResult(
                output, spec.mime, safeBaseName(item.name) + "_converted" + spec.extension);
    }

    private ConversionResult imagesToGif(
            List<SelectedItem> items, int requestedFps, int frameLimit) throws Exception {
        AnimationEdits edits = currentAnimationEdits();
        double sourceDurationSeconds = items.size() / (double) Math.max(1, requestedFps);
        List<AnimationEdits.TimeRange> keptRanges = edits.keptRanges(sourceDurationSeconds);
        List<SelectedItem> keptItems = new ArrayList<>();
        for (int i = 0; i < items.size() && keptItems.size() < frameLimit; i++) {
            double frameMidpoint = (i + 0.5) / Math.max(1.0, requestedFps);
            if (isTimeInsideRanges(frameMidpoint, keptRanges)) keptItems.add(items.get(i));
        }
        int count = keptItems.size();
        if (count <= 0) throw new IOException("分割删除后没有可用图片帧");

        boolean smartResolution = isSmartResolution();
        int[] requested = smartResolution
                ? gifMemorySafeBounds(960, 720)
                : selectedBounds(1280, 720, true);
        checkCancelled();
        Bitmap firstRaw = decodeBitmap(
                keptItems.get(0).uri, requested[0], requested[1], 24_000_000L);
        checkCancelled();
        if (firstRaw == null) throw new IOException("无法读取第一张图片");
        if (smartResolution) {
            requested = smartImageGifBounds(firstRaw, count, requestedFps);
        }
        int[] editedFirstSize = FrameEditor.editedSize(
                firstRaw.getWidth(), firstRaw.getHeight(), edits);
        int[] canvasSize = fitSize(
                editedFirstSize[0], editedFirstSize[1],
                requested[0], requested[1], true);
        int canvasWidth = Math.max(1, canvasSize[0]);
        int canvasHeight = Math.max(1, canvasSize[1]);

        File output = cacheFile(".gif");
        double playbackFps = Math.min(100.0, requestedFps * edits.speed);
        int delayMs = Math.max(10, (int) Math.round(1000.0 / playbackFps));
        ensureCacheCapacity(estimatedGifOutputBytes(canvasWidth, canvasHeight, count));
        int[] gifPixels = new int[canvasWidth * canvasHeight];
        byte[] gifIndexes = new byte[canvasWidth * canvasHeight];
        Bitmap renderedFrame = Bitmap.createBitmap(
                canvasWidth, canvasHeight, Bitmap.Config.ARGB_8888);
        Canvas renderedCanvas = new Canvas(renderedFrame);
        Paint editPaint = FrameEditor.createPaint(edits);

        try (OutputStream out = new BufferedOutputStream(
                     new FileOutputStream(output), 256 * 1024);
             FastGifEncoder encoder = new FastGifEncoder(
                     out, canvasWidth, canvasHeight, currentGifLoopCount(), this::isCancellationRequested)) {
            SeamlessGifWriter gifWriter = new SeamlessGifWriter(encoder, delayMs);
            for (int i = 0; i < count; i++) {
                checkCancelled();
                Bitmap raw = i == 0 ? firstRaw : decodeBitmap(
                        keptItems.get(i).uri,
                        Math.max(canvasWidth, requested[0]),
                        Math.max(canvasHeight, requested[1]), 24_000_000L);
                if (raw == null) continue;
                try {
                    FrameEditor.drawBitmap(
                            renderedCanvas, raw, 0xFFFFFFFF, edits, editPaint);
                    offerGifFrame(
                            encoder, gifWriter, renderedFrame, gifPixels, gifIndexes);
                } finally {
                    raw.recycle();
                }
                checkCancelled();
                updateProgress((int) ((i + 1) * 1000L / count),
                        "正在生成 GIF：" + (i + 1) + " / " + count);
            }
            checkCancelled();
            gifWriter.finishFrames(currentGifLoopCount() == 0);
            encoder.finish();
        } finally {
            if (!firstRaw.isRecycled()) firstRaw.recycle();
            renderedFrame.recycle();
        }
        checkCancelled();
        if (output.length() == 0) throw new IOException("GIF 生成失败");
        String name = items.size() == 1
                ? safeBaseName(items.get(0).name) + ".gif"
                : "images_to_gif.gif";
        return new ConversionResult(output, "image/gif", name);
    }

    private BatchConversionResult videosToGifBatch(
            List<SelectedItem> items, int requestedFps, int frameLimit,
            int videoLoops, int reverseLoop) throws Exception {
        List<PendingBatchFile> outputs = new ArrayList<>();
        Set<String> usedNames = new HashSet<>();
        try {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                int progressStart = (int) (i * 1000L / items.size());
                int progressEnd = (int) ((i + 1) * 1000L / items.size());
                updateProgress(progressStart,
                        "批量生成 GIF：" + (i + 1) + " / " + items.size());
                progressMapStart = progressStart;
                progressMapSpan = Math.max(1, progressEnd - progressStart);
                progressMapPrefix = "批量 " + (i + 1) + "/" + items.size() + " · ";
                ConversionResult result;
                try {
                    result = videosToGif(
                            Collections.singletonList(item), requestedFps, frameLimit,
                            videoLoops, reverseLoop);
                } finally {
                    progressMapStart = 0;
                    progressMapSpan = 1000;
                    progressMapPrefix = "";
                }
                String displayName = uniqueEntryName(
                        safeBaseName(item.name) + ".gif", usedNames);
                outputs.add(new PendingBatchFile(result.file, result.mime, displayName));
            }
            return new BatchConversionResult(outputs);
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        }
    }

    private ConversionResult videosToGif(
            List<SelectedItem> items, int requestedFps, int frameLimit,
            int videoLoops, int reverseLoop) throws Exception {
        videoLoops = GifPlaybackPlan.passCount(videoLoops, reverseLoop);
        if (frameLimit < videoLoops) throw new IOException("帧数上限小于循环轮次，请增加帧数上限");
        if (items.isEmpty()) throw new IOException("没有可转换的视频");
        for (SelectedItem item : items) {
            if (!item.isVideo()) throw new IOException("视频转 GIF 不能与图片混选");
        }

        final List<SelectedItem> originalItems = items;
        final AnimationEdits edits = currentAnimationEdits();
        final double startSeconds = edits.trimStartSeconds;
        final double durationSeconds = edits.trimDurationSeconds;

        updateProgress(5, "正在读取视频信息……");
        List<VideoFrameDecoder.Info> sourceInfos = new ArrayList<>();
        List<Long> sourceStartsUs = new ArrayList<>();
        List<Long> sourceEndsUs = new ArrayList<>();
        for (int i = 0; i < items.size(); i++) {
            checkCancelled();
            VideoFrameDecoder.Info info = VideoFrameDecoder.probe(this, items.get(i).uri);
            if (info.durationUs <= 0) {
                throw new IOException("无法读取视频时长：" + items.get(i).name);
            }
            long startUs = Math.min(Math.max(0L, Math.round(startSeconds * 1_000_000.0)),
                    Math.max(0L, info.durationUs - 1));
            long endUs = durationSeconds <= 0
                    ? info.durationUs
                    : Math.min(info.durationUs,
                            saturatingAdd(startUs,
                                    Math.max(1L, Math.round(
                                            durationSeconds * 1_000_000.0))));
            if (endUs <= startUs) {
                throw new IOException("截取时间范围无效：" + items.get(i).name);
            }
            sourceInfos.add(info);
            sourceStartsUs.add(startUs);
            sourceEndsUs.add(endUs);
            updateProgress(5 + (int) ((i + 1) * 45L / items.size()),
                    "读取视频信息：" + (i + 1) + " / " + items.size());
        }

        VideoTimeline timeline = buildVideoTimeline(
                items, sourceInfos, sourceStartsUs, sourceEndsUs, edits);
        final List<SelectedItem> timelineItems = timeline.items;
        final List<VideoFrameDecoder.Info> infos = timeline.infos;
        final List<Long> startsUs = timeline.startsUs;
        final List<Long> endsUs = timeline.endsUs;
        final List<Boolean> timelineReversed = timeline.reversed;
        if (timelineItems.isEmpty()) throw new IOException("分割删除后没有可用视频片段");

        long onePassDurationUs = 0L;
        for (int i = 0; i < startsUs.size(); i++) {
            onePassDurationUs = saturatingAdd(
                    onePassDurationUs, Math.max(1L, endsUs.get(i) - startsUs.get(i)));
        }
        double requestedOutputFps = Math.min(100.0, Math.max(1.0, requestedFps));
        long onePassRequestedFrames = Math.max(1L, (long) Math.ceil(
                onePassDurationUs * requestedOutputFps
                        / (1_000_000.0 * edits.speed)));

        long totalRequested = Math.max(1L,
                saturatingMultiply(onePassRequestedFrames, Math.max(1, videoLoops)));
        long[] segmentDurations = new long[startsUs.size()];
        for (int i=0;i<segmentDurations.length;i++) segmentDurations[i]=Math.max(1L,endsUs.get(i)-startsUs.get(i));
        int[] allocatedFrames=GifPlaybackPlan.allocateSegments(segmentDurations,edits.speed,
                requestedFps,frameLimit,videoLoops);
        long allocatedOnePass=0;for(int count:allocatedFrames)allocatedOnePass+=count;
        double actualFps=Math.min(100,allocatedOnePass*1e6*edits.speed/onePassDurationUs);
        final double finalActualFps = actualFps;
        final double sourceSampleFps = Math.max(0.2,
                Math.min(240.0, finalActualFps / edits.speed));

        VideoFrameDecoder.Info firstInfo = infos.get(0);
        long smartOutputFrames = Math.max(1L, Math.min((long) frameLimit, totalRequested));
        int[] requested = isSmartResolution()
                ? smartVideoGifBounds(
                        timelineItems, infos, startsUs, endsUs, smartOutputFrames)
                : selectedBounds(
                        FrameEditor.editedSize(
                                firstInfo.orientedWidth(), firstInfo.orientedHeight(), edits)[0],
                        FrameEditor.editedSize(
                                firstInfo.orientedWidth(), firstInfo.orientedHeight(), edits)[1],
                        true);
        int[] editedFirstSize = FrameEditor.editedSize(
                firstInfo.orientedWidth(), firstInfo.orientedHeight(), edits);
        int[] canvasSize = fitSize(
                editedFirstSize[0], editedFirstSize[1],
                requested[0], requested[1], true);
        final int canvasWidth = Math.max(1, canvasSize[0]);
        final int canvasHeight = Math.max(1, canvasSize[1]);
        int delayMs = Math.max(10, (int) Math.round(1000.0 / actualFps));
        if (isSmartResolution()) {
            updateProgress(50, "智能推荐：" + canvasWidth + "×" + canvasHeight
                    + "，约 " + smartOutputFrames + " 帧");
        }

        List<Integer> segmentFrameCounts = new ArrayList<>();
        long plannedOnePass = 0;
        for (int i = 0; i < startsUs.size(); i++) {
            int count = allocatedFrames[i];
            segmentFrameCounts.add(count);
            plannedOnePass += count;
        }
        final int plannedTotalFrames = (int) Math.max(1L,
                Math.min((long) frameLimit,
                        saturatingMultiply(plannedOnePass, Math.max(1L, videoLoops))));
        final int[] emittedTotal = {0};

        boolean needsIndexedCache = videoLoops > 1 || reverseLoop != 0;
        for (boolean reversed : timelineReversed) {
            if (reversed) {
                needsIndexedCache = true;
                break;
            }
        }

        long canvasPixels = (long) canvasWidth * canvasHeight;
        long outputEstimate = estimatedGifOutputBytes(
                canvasWidth, canvasHeight, plannedTotalFrames);
        long indexedCacheEstimate = needsIndexedCache
                ? saturatingMultiply(canvasPixels,
                        Math.min((long) frameLimit, plannedOnePass))
                : 0L;
        ensureCacheCapacity(saturatingAdd(outputEstimate, indexedCacheEstimate));

        File output = cacheFile(".gif");
        int[] gifPixels = new int[canvasWidth * canvasHeight];
        byte[] gifIndexes = new byte[canvasWidth * canvasHeight];
        Bitmap renderedFrame = Bitmap.createBitmap(
                canvasWidth, canvasHeight, Bitmap.Config.ARGB_8888);
        Canvas renderedCanvas = new Canvas(renderedFrame);
        Paint editPaint = FrameEditor.createPaint(edits);

        try (OutputStream out = new BufferedOutputStream(
                     new FileOutputStream(output), 256 * 1024);
             FastGifEncoder encoder = new FastGifEncoder(
                     out, canvasWidth, canvasHeight, currentGifLoopCount(), this::isCancellationRequested)) {
            SeamlessGifWriter gifWriter = new SeamlessGifWriter(encoder, delayMs);
            if (!needsIndexedCache) {
                for (int itemIndex = 0;
                     itemIndex < timelineItems.size()
                             && emittedTotal[0] < plannedTotalFrames;
                     itemIndex++) {
                    checkCancelled();
                    SelectedItem item = timelineItems.get(itemIndex);
                    int remaining = plannedTotalFrames - emittedTotal[0];
                    int expectedNow = Math.min(
                            segmentFrameCounts.get(itemIndex), remaining);
                    String prefix = "第 " + (itemIndex + 1) + "/"
                            + timelineItems.size() + " 段";
                    if (itemIndex > 0) gifWriter.markSegmentBoundary();

                    final long segmentStartUs = startsUs.get(itemIndex);
                    final int[] emittedSegment = {0};
                    final boolean[] hasIndexedFrame = {false};
                    int[] decodeBounds = FrameEditor.decodeBounds(
                            infos.get(itemIndex).orientedWidth(),
                            infos.get(itemIndex).orientedHeight(),
                            canvasWidth, canvasHeight, edits);

                    VideoFrameDecoder.decode(
                            this, item.uri, segmentStartUs, endsUs.get(itemIndex),
                            sourceSampleFps, expectedNow,
                            decodeBounds[0], decodeBounds[1],
                            this::isCancellationRequested,
                            (bitmap, index, expected, ptsUs) -> {
                                checkCancelled();
                                try {
                                    FrameEditor.drawBitmap(
                                            renderedCanvas, bitmap, 0xFFFFFFFF,
                                            edits, editPaint);
                                    renderedFrame.getPixels(
                                            gifPixels, 0, canvasWidth,
                                            0, 0, canvasWidth, canvasHeight);
                                    encoder.indexPixels(gifPixels, gifIndexes);
                                    hasIndexedFrame[0] = true;
                                } finally {
                                    bitmap.recycle();
                                }
                                int desired = desiredFramesAtPresentation(
                                        ptsUs, segmentStartUs, expectedNow,
                                        finalActualFps, edits.speed);
                                while (emittedSegment[0] < desired
                                        && emittedTotal[0] < plannedTotalFrames) {
                                    gifWriter.offer(gifIndexes);
                                    emittedSegment[0]++;
                                    emittedTotal[0]++;
                                }
                                int progress = 50 + (int) (emittedTotal[0] * 940L
                                        / plannedTotalFrames);
                                updateProgress(Math.min(990, progress),
                                        prefix + "：已完成 " + emittedTotal[0] + " / "
                                                + plannedTotalFrames + " 帧（"
                                                + String.format(
                                                        Locale.CHINA, "%.1f", finalActualFps)
                                                + " FPS）");
                            });
                    while (hasIndexedFrame[0]
                            && emittedSegment[0] < expectedNow
                            && emittedTotal[0] < plannedTotalFrames) {
                        gifWriter.offer(gifIndexes);
                        emittedSegment[0]++;
                        emittedTotal[0]++;
                    }
                }
            } else {
                List<IndexedFrameStore> segmentStores = new ArrayList<>();
                List<IndexedFrameStore> uniqueStores = new ArrayList<>();
                List<Integer> decodeItemIndexes = new ArrayList<>();
                java.util.Map<String, IndexedFrameStore> cacheByKey =
                        new java.util.HashMap<>();
                int cacheExpected = 0;

                try {
                    for (int i = 0; i < timelineItems.size(); i++) {
                        String key = timelineItems.get(i).uri.toString()
                                + '\n' + startsUs.get(i)
                                + '\n' + endsUs.get(i)
                                + '\n' + segmentFrameCounts.get(i);
                        IndexedFrameStore store = cacheByKey.get(key);
                        if (store == null) {
                            store = new IndexedFrameStore(
                                    new File(getCacheDir(),
                                            "gif_frames_" + System.nanoTime() + ".cache"),
                                    encoder.pixelCount(),
                                    this::isCancellationRequested);
                            cacheByKey.put(key, store);
                            uniqueStores.add(store);
                            decodeItemIndexes.add(i);
                            cacheExpected += segmentFrameCounts.get(i);
                        }
                        segmentStores.add(store);
                    }

                    final int expectedCacheFrames = Math.max(1, cacheExpected);
                    final int[] cachedFrames = {0};
                    for (int decodePosition = 0;
                         decodePosition < decodeItemIndexes.size();
                         decodePosition++) {
                        checkCancelled();
                        int itemIndex = decodeItemIndexes.get(decodePosition);
                        SelectedItem item = timelineItems.get(itemIndex);
                        IndexedFrameStore store = segmentStores.get(itemIndex);
                        int expectedNow = segmentFrameCounts.get(itemIndex);
                        String prefix = "缓存第 " + (decodePosition + 1) + "/"
                                + decodeItemIndexes.size() + " 段";

                        final long segmentStartUs = startsUs.get(itemIndex);
                        final int[] cachedSegment = {0};
                        final boolean[] hasIndexedFrame = {false};
                        int[] decodeBounds = FrameEditor.decodeBounds(
                                infos.get(itemIndex).orientedWidth(),
                                infos.get(itemIndex).orientedHeight(),
                                canvasWidth, canvasHeight, edits);
                        VideoFrameDecoder.decode(
                                this, item.uri,
                                segmentStartUs, endsUs.get(itemIndex),
                                sourceSampleFps, expectedNow,
                                decodeBounds[0], decodeBounds[1],
                                this::isCancellationRequested,
                                (bitmap, index, expected, ptsUs) -> {
                                    checkCancelled();
                                    try {
                                        FrameEditor.drawBitmap(
                                                renderedCanvas, bitmap, 0xFFFFFFFF,
                                                edits, editPaint);
                                        renderedFrame.getPixels(
                                                gifPixels, 0, canvasWidth,
                                                0, 0, canvasWidth, canvasHeight);
                                        encoder.indexPixels(gifPixels, gifIndexes);
                                        hasIndexedFrame[0] = true;
                                    } finally {
                                        bitmap.recycle();
                                    }
                                    int desired = desiredFramesAtPresentation(
                                            ptsUs, segmentStartUs, expectedNow,
                                            finalActualFps, edits.speed);
                                    while (cachedSegment[0] < desired) {
                                        store.add(gifIndexes);
                                        cachedSegment[0]++;
                                        cachedFrames[0]++;
                                    }
                                    int progress = 50 + (int) (cachedFrames[0] * 350L
                                            / expectedCacheFrames);
                                    updateProgress(Math.min(400, progress),
                                            prefix + "：" + (index + 1) + " / "
                                                    + expected + " 帧");
                                });
                        while (hasIndexedFrame[0] && cachedSegment[0] < expectedNow) {
                            store.add(gifIndexes);
                            cachedSegment[0]++;
                            cachedFrames[0]++;
                        }
                        if (store.size() == 0) {
                            throw new IOException(
                                    "没有从视频中解码到可用帧：" + item.name);
                        }
                    }

                    for (int pass = 1;
                         pass <= videoLoops
                                 && emittedTotal[0] < plannedTotalFrames;
                         pass++) {
                        checkCancelled();
                        boolean reverseWholePass = GifPlaybackPlan.reversed(pass, reverseLoop);
                        for (int sequencePos = 0;
                             sequencePos < timelineItems.size()
                                     && emittedTotal[0] < plannedTotalFrames;
                             sequencePos++) {
                            int itemIndex = reverseWholePass
                                    ? timelineItems.size() - 1 - sequencePos
                                    : sequencePos;
                            SelectedItem item = timelineItems.get(itemIndex);
                            IndexedFrameStore store = segmentStores.get(itemIndex);
                            // Reverse the edited timeline: a second reverse restores local forward order.
                            boolean reverseSegment = timelineReversed.get(itemIndex)
                                    ^ reverseWholePass;
                            int count = store.size();
                            String prefix = "第 " + pass + "/" + videoLoops
                                    + " 轮 · " + (sequencePos + 1) + "/"
                                    + timelineItems.size() + " 段";
                            if (emittedTotal[0] > 0) {
                                gifWriter.markSegmentBoundary();
                            }

                            for (int position = 0;
                                 position < count
                                         && emittedTotal[0] < plannedTotalFrames;
                                 position++) {
                                checkCancelled();
                                int frameIndex = reverseSegment
                                        ? count - 1 - position : position;
                                store.read(frameIndex, gifIndexes);
                                gifWriter.offer(gifIndexes);
                                emittedTotal[0]++;
                                int progress = 400 + (int) (emittedTotal[0] * 590L
                                        / plannedTotalFrames);
                                updateProgress(Math.min(990, progress),
                                        prefix + "：已写入 " + emittedTotal[0]
                                                + " / " + plannedTotalFrames + " 帧");
                            }
                        }
                    }
                } finally {
                    for (IndexedFrameStore store : uniqueStores) store.close();
                }
            }

            checkCancelled();
            if (emittedTotal[0] <= 0) {
                throw new IOException("没有解码到可用视频帧");
            }
            updateProgress(995, "正在优化循环接缝并完成 GIF……");
            gifWriter.finishFrames(currentGifLoopCount() == 0);
            if (gifWriter.writtenFrames() <= 0) {
                throw new IOException("没有可写入的 GIF 帧");
            }
            encoder.finish();
        } finally {
            renderedFrame.recycle();
        }

        checkCancelled();
        if (output.length() == 0) throw new IOException("GIF 生成失败");
        String name = originalItems.size() == 1 && videoLoops == 1
                ? safeBaseName(originalItems.get(0).name) + ".gif"
                : "videos_to_gif.gif";
        return new ConversionResult(output, "image/gif", name);
    }

    private VideoTimeline buildVideoTimeline(
            List<SelectedItem> items,
            List<VideoFrameDecoder.Info> infos,
            List<Long> startsUs,
            List<Long> endsUs,
            AnimationEdits edits) {
        // Split points are selected against the full preview timeline. Intersect them with each
        // clip's trimmed source window so combining trim + split/delete never shifts a cut.
        double totalSourceSeconds = 0.0;
        for (VideoFrameDecoder.Info info : infos) {
            totalSourceSeconds += Math.max(0L, info.durationUs) / 1_000_000.0;
        }
        List<AnimationEdits.PlaybackRange> playbackRanges =
                edits.playbackRanges(0.0, totalSourceSeconds);
        VideoTimeline timeline = new VideoTimeline();
        double itemSourceTimelineStart = 0.0;
        for (int i = 0; i < items.size(); i++) {
            long sourceStartUs = startsUs.get(i);
            long sourceEndUs = endsUs.get(i);
            double fullSourceDuration = Math.max(0L, infos.get(i).durationUs)
                    / 1_000_000.0;
            double trimmedTimelineStart = itemSourceTimelineStart
                    + sourceStartUs / 1_000_000.0;
            double trimmedTimelineEnd = itemSourceTimelineStart
                    + sourceEndUs / 1_000_000.0;
            List<VideoSlice> slices = new ArrayList<>();
            for (AnimationEdits.PlaybackRange playback : playbackRanges) {
                double intersectionStart = Math.max(
                        trimmedTimelineStart, playback.startSeconds);
                double intersectionEnd = Math.min(
                        trimmedTimelineEnd, playback.endSeconds);
                if (intersectionEnd - intersectionStart < 0.001) continue;
                long localStartUs = Math.round(
                        (intersectionStart - itemSourceTimelineStart) * 1_000_000.0);
                long localEndUs = Math.round(
                        (intersectionEnd - itemSourceTimelineStart) * 1_000_000.0);
                localStartUs = Math.max(sourceStartUs, Math.min(sourceEndUs - 1, localStartUs));
                localEndUs = Math.max(localStartUs + 1, Math.min(sourceEndUs, localEndUs));
                slices.add(new VideoSlice(
                        localStartUs, localEndUs, playback.reversed));
            }
            if (items.get(i).reversed) {
                Collections.reverse(slices);
                List<VideoSlice> reversedSlices = new ArrayList<>();
                for (VideoSlice slice : slices) {
                    reversedSlices.add(new VideoSlice(
                            slice.startUs, slice.endUs, true));
                }
                slices = reversedSlices;
            }
            for (VideoSlice slice : slices) {
                timeline.items.add(items.get(i));
                timeline.infos.add(infos.get(i));
                timeline.startsUs.add(slice.startUs);
                timeline.endsUs.add(slice.endUs);
                timeline.reversed.add(slice.reversed);
            }
            itemSourceTimelineStart += fullSourceDuration;
        }
        return timeline;
    }

    private static int desiredFramesAtPresentation(
            long presentationUs, long segmentStartUs, int expectedFrames,
            double outputFps, double speed) {
        double sourceElapsedUs = Math.max(0L, presentationUs - segmentStartUs);
        long desired = 1L + (long) Math.floor(
                sourceElapsedUs * outputFps / (1_000_000.0 * speed));
        return (int) Math.max(1L, Math.min((long) expectedFrames, desired));
    }

    private static boolean isTimeInsideRanges(
            double second, List<AnimationEdits.TimeRange> ranges) {
        for (AnimationEdits.TimeRange range : ranges) {
            if (second >= range.startSeconds && second < range.endSeconds) return true;
        }
        return false;
    }

    private ConversionResult gifToMp4(
            Uri uri, String name, int requestedFps, int frameLimit,
            int bitrate, int loops, int outputFormat) throws Exception {
        VideoCodecSpec codecSpec = videoCodecSpec(outputFormat);
        if (!Mp4Encoder.hasSurfaceEncoder(codecSpec.mime)) {
            throw new IOException("本机没有可用的 " + codecSpec.label + " 硬件或系统编码器");
        }
        File output = cacheFile(".mp4");
        AnimationEdits edits = currentAnimationEdits();
        GifDrawable gif = null;
        Bitmap frameBitmap = null;
        Bitmap sourceBitmap = null;
        try {
            gif = new GifDrawable(getContentResolver(), uri);
            gif.stop();
            int sourceWidth = Math.max(1, gif.getIntrinsicWidth());
            int sourceHeight = Math.max(1, gif.getIntrinsicHeight());
            int durationMs = Math.max(1, gif.getDuration());
            int clipStartMs = Math.min(durationMs - 1,
                    Math.max(0, (int) Math.round(edits.trimStartSeconds * 1000.0)));
            int clipEndMs = edits.trimDurationSeconds <= 0.0
                    ? durationMs
                    : Math.min(durationMs, clipStartMs + Math.max(1,
                            (int) Math.round(edits.trimDurationSeconds * 1000.0)));
            double clipStartSeconds = clipStartMs / 1000.0;
            double clipEndSeconds = clipEndMs / 1000.0;
            double keptDurationSeconds = edits.keptDurationSeconds(
                    clipStartSeconds, clipEndSeconds);
            if (keptDurationSeconds <= 0.0005) {
                throw new IOException("分割删除后没有可用 GIF 片段");
            }

            int[] editedSourceSize = FrameEditor.editedSize(
                    sourceWidth, sourceHeight, edits);
            int[] requested = selectedBounds(
                    editedSourceSize[0], editedSourceSize[1], false);
            int[] size = fitSize(
                    editedSourceSize[0], editedSourceSize[1],
                    requested[0], requested[1], false);
            size[0] = makeEven(Math.max(16, size[0]));
            size[1] = makeEven(Math.max(16, size[1]));

            double totalOutputDurationSeconds = keptDurationSeconds
                    * Math.max(1, loops) / edits.speed;
            int requestedCount = Math.max(1,
                    (int) Math.ceil(totalOutputDurationSeconds * requestedFps));
            int frameCount = Math.min(frameLimit, requestedCount);
            double actualFps = frameCount / totalOutputDurationSeconds;
            int encoderFps = Math.max(1, Math.min(120, (int) Math.round(actualFps)));

            try (Mp4Encoder encoder = new Mp4Encoder(
                    output, size[0], size[1], encoderFps, bitrate,
                    codecSpec.mime, codecSpec.label)) {
                frameBitmap = Bitmap.createBitmap(
                        encoder.width, encoder.height, Bitmap.Config.ARGB_8888);
                Canvas canvas = new Canvas(frameBitmap);
                Canvas sourceCanvas = null;
                Paint editPaint = FrameEditor.createPaint(edits);
                if (edits.hasVisualEdits()) {
                    int[] decodeBounds = FrameEditor.decodeBounds(
                            sourceWidth, sourceHeight,
                            encoder.width, encoder.height, edits);
                    sourceBitmap = Bitmap.createBitmap(
                            decodeBounds[0], decodeBounds[1], Bitmap.Config.ARGB_8888);
                    sourceCanvas = new Canvas(sourceBitmap);
                    gif.setBounds(0, 0, sourceBitmap.getWidth(), sourceBitmap.getHeight());
                } else {
                    int[] drawSize = fitSize(
                            sourceWidth, sourceHeight,
                            encoder.width, encoder.height, true);
                    int left = (encoder.width - drawSize[0]) / 2;
                    int top = (encoder.height - drawSize[1]) / 2;
                    gif.setBounds(left, top, left + drawSize[0], top + drawSize[1]);
                }

                for (int i = 0; i < frameCount; i++) {
                    checkCancelled();
                    double outputTimeSeconds = frameCount <= 1
                            ? 0.0
                            : i * totalOutputDurationSeconds / frameCount;
                    double keptTimelineSecond = (outputTimeSeconds * edits.speed)
                            % keptDurationSeconds;
                    double sourceSecond = edits.sourceSecondAtKeptOffset(
                            clipStartSeconds, clipEndSeconds, keptTimelineSecond);
                    int gifTimeMs = Math.min(durationMs - 1,
                            (int) Math.round(sourceSecond * 1000.0));
                    gif.seekToBlocking(gifTimeMs);
                    checkCancelled();
                    if (sourceBitmap != null && sourceCanvas != null) {
                        sourceCanvas.drawColor(0xFF000000);
                        gif.draw(sourceCanvas);
                        FrameEditor.drawBitmap(
                                canvas, sourceBitmap, 0xFF000000, edits, editPaint);
                    } else {
                        canvas.drawColor(0xFF000000);
                        gif.draw(canvas);
                    }
                    long presentationUs = Math.round(outputTimeSeconds * 1_000_000.0);
                    encoder.encodeFrame(frameBitmap, presentationUs);
                    checkCancelled();
                    updateProgress((int) ((i + 1) * 1000L / frameCount),
                            String.format(Locale.CHINA,
                                    "GIF 转 %s MP4：%d / %d 帧，%dx%d，%.1f Mbps",
                                    codecSpec.shortLabel, i + 1, frameCount,
                                    encoder.width, encoder.height,
                                    encoder.bitrate / 1_000_000.0));
                }
                encoder.finish();
            }
        } finally {
            if (sourceBitmap != null) sourceBitmap.recycle();
            if (frameBitmap != null) frameBitmap.recycle();
            if (gif != null) gif.recycle();
        }

        if (output.length() == 0) throw new IOException("MP4 生成失败");
        return new ConversionResult(
                output, "video/mp4",
                safeBaseName(name) + "_" + codecSpec.fileSuffix + ".mp4");
    }


    private BatchConversionResult convertStaticBatchFiles(
            List<SelectedItem> items, int format, int quality,
            boolean keepOriginalResolution, boolean qualityWasTouched) throws Exception {
        OutputSpec spec = outputSpec(format);
        List<PendingBatchFile> outputs = new ArrayList<>();
        Set<String> usedNames = new HashSet<>();
        try {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                String displayName = uniqueEntryName(
                        safeBaseName(item.name) + "_converted" + spec.extension, usedNames);
                File output = cacheFile(spec.extension);
                try (OutputStream out = new BufferedOutputStream(
                        new FileOutputStream(output), 256 * 1024)) {
                    if (isExactNoOp(item, format, keepOriginalResolution, qualityWasTouched)) {
                        copyUriToStream(item.uri, out);
                    } else {
                        int[] bounds = selectedBounds(0, 0, false);
                        Bitmap bitmap = decodeBitmap(item.uri, bounds[0], bounds[1], 80_000_000L);
                        checkCancelled();
                        if (bitmap == null) throw new IOException("无法解码：" + item.name);
                        try {
                            ensureCacheCapacity(estimatedStaticOutputBytes(
                                    format, bitmap.getWidth(), bitmap.getHeight()));
                            int effectiveQuality = resolvedImageQuality(
                                    item, bitmap, format, quality, qualityWasTouched);
                            encodeBitmap(bitmap, format, effectiveQuality, out);
                        } finally {
                            bitmap.recycle();
                        }
                    }
                }
                checkCancelled();
                if (output.length() == 0) throw new IOException("输出文件为空：" + item.name);
                outputs.add(new PendingBatchFile(output, spec.mime, displayName));
                updateProgress((int) ((i + 1) * 1000L / items.size()),
                        "批量转换：" + (i + 1) + " / " + items.size());
            }
            return new BatchConversionResult(outputs);
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        }
    }

    private ConversionResult convertStaticBatch(
            List<SelectedItem> items, int format, int quality,
            boolean keepOriginalResolution, boolean qualityWasTouched) throws Exception {
        OutputSpec spec = outputSpec(format);
        File output = cacheFile(".zip");
        Set<String> usedNames = new HashSet<>();
        try (ZipOutputStream zip = new ZipOutputStream(
                new BufferedOutputStream(
                        new FileOutputStream(output), 256 * 1024))) {
            zip.setLevel(Deflater.BEST_SPEED);
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                String entryName = uniqueEntryName(
                        safeBaseName(item.name) + spec.extension, usedNames);
                zip.putNextEntry(new ZipEntry(entryName));
                if (isExactNoOp(item, format, keepOriginalResolution, qualityWasTouched)) {
                    copyUriToStream(item.uri, zip);
                } else {
                    int[] bounds = selectedBounds(0, 0, false);
                    Bitmap bitmap = decodeBitmap(item.uri, bounds[0], bounds[1], 80_000_000L);
                    checkCancelled();
                    if (bitmap == null) throw new IOException("无法解码：" + item.name);
                    try {
                        ensureCacheCapacity(estimatedStaticOutputBytes(
                                format, bitmap.getWidth(), bitmap.getHeight()));
                        int effectiveQuality = resolvedImageQuality(
                                item, bitmap, format, quality, qualityWasTouched);
                        encodeBitmap(bitmap, format, effectiveQuality, zip);
                    } finally {
                        bitmap.recycle();
                    }
                }
                zip.closeEntry();
                updateProgress((int) ((i + 1) * 1000L / items.size()),
                        "批量转换：" + (i + 1) + " / " + items.size());
            }
        }
        checkCancelled();
        if (output.length() == 0) throw new IOException("ZIP 生成失败");
        return new ConversionResult(output, "application/zip",
                "converted_" + spec.shortName.toLowerCase(Locale.ROOT)
                        + "_" + items.size() + "_files.zip");
    }

    // ===================== 文本格式转换（Markdown / HTML / CSV / TSV / JSON / YAML / XML / SRT / VTT） =====================

    private static final long MAX_TEXT_INPUT_BYTES = 64L * 1024 * 1024;

    /** Text output formats occupy spinner positions 13 (TXT) .. 23 (text-to-PDF). */
    private static final int TEXT_FORMAT_FIRST = 13;
    private static final int TEXT_FORMAT_LAST = 28;

    private static final String[] TEXT_OUTPUT_NAMES = {
            "TXT 纯文本",
            "HTML 网页",
            "CSV 表格",
            "JSON",
            "YAML",
            "XML",
            "Markdown 表格",
            "TSV 表格",
            "VTT 字幕",
            "SRT 字幕",
            "PDF 文档", "DOCX 文档", "EPUB 电子书", "ODT 文档", "WAV 音频", "RTF 文档"
    };
    private static final String[] TEXT_OUTPUT_HINTS = {
            "Markdown/HTML 去掉语法符号只留正文；CSV/TSV 转对齐表格；JSON 格式化缩进；XML 提取文字；字幕转纯文稿。",
            "Markdown 转带样式独立网页；CSV/TSV 生成表格网页；JSON 生成带高亮排版的预览页。",
            "JSON 数组转表格；Markdown 提取文档中的表格；TSV 直接转换；YAML 列表转表格。输出标准 CSV。",
            "CSV/TSV 每行转对象；Markdown 表格转 JSON；YAML/XML 转为 JSON 结构；字幕转字幕块 JSON。",
            "JSON 树转为缩进优雅的 YAML；CSV/TSV/Markdown 表格转为 YAML 记录列表。",
            "JSON/YAML 树转为缩进排版的 XML；表格数据转为记录式 XML，属性与文本自动处理。",
            "CSV/TSV 转为 Markdown 表格；JSON/YAML 的对象数组转为表格。",
            "CSV 转为制表符分隔的 TSV；Markdown/JSON/YAML 表格同样支持。",
            "SRT 字幕转 WebVTT：时间轴统一为点号毫秒，自动重编号，标签自动清理。",
            "WebVTT 字幕转 SRT：时间轴统一为逗号毫秒，自动重编号，标签自动清理。",
            "文本排成 A4 纸 PDF：自动分页，可选择与复制文字。",
            "提取正文生成 DOCX；复杂版式、图片与公式不保留。",
            "提取正文生成 EPUB 电子书；按阅读顺序提取章节。",
            "提取正文生成 ODT；复杂版式、图片与公式不保留。",
            "48 kHz / 16 bit 双声道 PCM",
            "提取正文生成支持中文的 RTF 文档。"
    };
    private static final String[] TEXT_OUTPUT_REQUIREMENTS = {
            "TXT 输出接受 Markdown、HTML、CSV、TSV、JSON、XML 和 SRT/VTT 字幕；TXT 与 YAML 本身已是纯文本，无需再转。",
            "HTML 输出接受 Markdown、CSV、TSV 和 JSON，请移除其他类型的文本文件。",
            "CSV 输出接受 JSON 数组、Markdown 表格、TSV 和 YAML 列表，请移除其他类型的文本文件。",
            "JSON 输出接受 CSV/TSV、Markdown 表格、YAML、XML 和 SRT/VTT 字幕，请移除其他类型的文本文件。",
            "YAML 输出接受 JSON、CSV/TSV 和含表格的 Markdown，请移除其他类型的文本文件。",
            "XML 输出接受 JSON、YAML、CSV/TSV 和含表格的 Markdown，请移除其他类型的文本文件。",
            "Markdown 输出接受 CSV/TSV 表格和 JSON/YAML 的对象数组，请移除其他类型的文本文件。",
            "TSV 输出接受 CSV、含表格的 Markdown 和 JSON/YAML 的对象数组，请移除其他类型的文本文件。",
            "VTT 输出只接受 SRT 字幕文件，请移除其他文件。",
            "SRT 输出只接受 WebVTT 字幕文件，请移除其他文件。",
            "文本转 PDF 接受所有文本类文件、DOCX/EPUB/ODT。",
            "请选择文本、PDF、DOCX、EPUB 或 ODT。",
            "请选择文本、PDF、DOCX、EPUB 或 ODT。",
            "请选择文本、PDF、DOCX、EPUB 或 ODT。",
            "请选择音频或视频。",
            "请选择文本、PDF、DOCX、EPUB 或 ODT。"
    };

    /** True for the eleven text output formats (13-23). */
    private boolean isTextOutputFormat(int format) {
        return (format >= TEXT_FORMAT_FIRST && format <= TEXT_FORMAT_LAST && format != 27) || format == 35 || format == 36;
    }

    /** True for the ten text input formats detected from file name / mime type. */
    private static boolean isTextSourceFormat(SourceFormat format) {
        return format == SourceFormat.MARKDOWN || format == SourceFormat.HTML
                || format == SourceFormat.CSV || format == SourceFormat.JSON
                || format == SourceFormat.TXT || format == SourceFormat.TSV
                || format == SourceFormat.YAML || format == SourceFormat.XML
                || format == SourceFormat.SRT || format == SourceFormat.VTT
                || format == SourceFormat.DOCX || format == SourceFormat.EPUB || format == SourceFormat.ODT
                || format == SourceFormat.RTF || format == SourceFormat.FB2 || format == SourceFormat.JSONL;
    }

    private String textFormatBadge(SourceFormat format) {
        switch (format) {
            case RTF: return "RTF";
            case FB2: return "FB2";
            case JSONL: return "JSONL";
            case DOCX: return "DOCX";
            case EPUB: return "EPUB";
            case ODT: return "ODT";
            case AUDIO: return "音频";
            case MARKDOWN: return "MD";
            case HTML: return "HTML";
            case CSV: return "CSV";
            case JSON: return "JSON";
            case TSV: return "TSV";
            case YAML: return "YAML";
            case XML: return "XML";
            case SRT: return "SRT";
            case VTT: return "VTT";
            default: return "TXT";
        }
    }

    /** Reads the whole document through SAF with a hard size guard for text conversions. */
    private byte[] readAllBytes(Uri uri, long maxBytes) throws IOException {
        try (InputStream in = getContentResolver().openInputStream(uri)) {
            if (in == null) throw new IOException("无法读取文件");
            ByteArrayOutputStream buffer = new ByteArrayOutputStream(64 * 1024);
            byte[] chunk = new byte[64 * 1024];
            long total = 0;
            int read;
            while ((read = in.read(chunk)) != -1) {
                if (isCancellationRequested()) throw new java.io.InterruptedIOException("已取消");
                total += read;
                if (total > maxBytes) {
                    throw new IOException("文件过大（超过 " + (maxBytes / (1024L * 1024L))
                            + " MB），文本转换暂不支持");
                }
                buffer.write(chunk, 0, read);
            }
            return buffer.toByteArray();
        }
    }

    /** Converts one text document according to the selected output format. */
    private ConversionResult convertTextDocument(SelectedItem item, int format, int quality,
                                                 boolean qualityTouched) throws Exception {
        OutputSpec spec = outputSpec(format);
        updateProgress(4, "正在读取 " + item.name + "……");
        String source;
        if (item.sourceFormat == SourceFormat.PDF || item.sourceFormat == SourceFormat.DOCX
                || item.sourceFormat == SourceFormat.EPUB || item.sourceFormat == SourceFormat.ODT) {
            source = DocumentKit.read(this, item.uri, item.sourceFormat.name(), this::checkCancelled);
        } else {
            byte[] input = readAllBytes(item.uri, MAX_TEXT_INPUT_BYTES);
            source = item.sourceFormat == SourceFormat.RTF ? new String(input, java.nio.charset.StandardCharsets.ISO_8859_1) : TextConverter.decode(input);
        }
        if (item.sourceFormat == SourceFormat.RTF || item.sourceFormat == SourceFormat.FB2 || item.sourceFormat == SourceFormat.JSONL) {
            SourceFormat original=item.sourceFormat;
            source=original == SourceFormat.RTF ? ExtraTextFormats.rtfText(source)
                    : original == SourceFormat.FB2 ? ExtraTextFormats.fb2Text(source) : ExtraTextFormats.jsonlToJson(source);
            item=new SelectedItem(item.uri,item.name,item.mime,item.size,
                    original == SourceFormat.JSONL ? SourceFormat.JSON : SourceFormat.TXT);
        }
        checkCancelled();
        if (source.trim().isEmpty()) {
            throw new IOException("文件是空的，没有可转换的内容：" + item.name);
        }
        checkCancelled();
        if (format == 24 || format == 25 || format == 26 || format == 28) {
            String plain = plainTextProjection(item, source);
            File output = cacheFile(outputSpec(format).extension);
            DocumentKit.write(output, format, plain, safeBaseName(item.name), this::checkCancelled);
            return new ConversionResult(output, outputSpec(format).mime,
                    safeBaseName(item.name) + outputSpec(format).extension);
        }
        if (format == 23) {
            return textToPdfDocument(item, source, quality, qualityTouched);
        }
        updateProgress(300, "正在转换文本格式……");
        String result;
        switch (format) {
            case 35:
                result=ExtraTextFormats.jsonToJsonl(item.sourceFormat == SourceFormat.JSON ? source : convertToJsonText(item,source));
                break;
            case 36:
                result=ExtraTextFormats.fb2(plainTextProjection(item,source),safeBaseName(item.name));
                break;
            case 13:
                result = convertToPlainText(item, source);
                break;
            case 14:
                result = convertToHtmlPage(item, source);
                break;
            case 15:
                result = convertToCsvText(item, source);
                break;
            case 16:
                result = convertToJsonText(item, source);
                break;
            case 17:
                result = convertToYamlText(item, source);
                break;
            case 18:
                result = convertToXmlText(item, source);
                break;
            case 19:
                result = convertToMarkdownText(item, source);
                break;
            case 20:
                result = convertToTsvText(item, source);
                break;
            case 21:
                if (item.sourceFormat != SourceFormat.SRT) {
                    throw new IOException("VTT 输出只接受 SRT 字幕文件：" + item.name);
                }
                result = SubtitleKit.srtToVtt(source);
                break;
            case 22:
                if (item.sourceFormat != SourceFormat.VTT) {
                    throw new IOException("SRT 输出只接受 WebVTT 字幕文件：" + item.name);
                }
                result = SubtitleKit.vttToSrt(source);
                break;
            default:
                throw new IllegalArgumentException("未知文本输出格式");
        }
        checkCancelled();
        if (result == null || result.trim().isEmpty()) {
            throw new IOException("转换结果为空：" + item.name);
        }
        updateProgress(880, "正在写入输出文件……");
        File output = cacheFile(spec.extension);
        try (OutputStream out = new BufferedOutputStream(
                new FileOutputStream(output), 64 * 1024)) {
            out.write(result.getBytes(StandardCharsets.UTF_8));
        }
        if (output.length() == 0) throw new IOException("写入失败：" + item.name);
        return new ConversionResult(output, spec.mime, safeBaseName(item.name) + spec.extension);
    }

    /** 13: every supported source down to clean plain text. */
    private String convertToPlainText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case PDF: case DOCX: case EPUB: case ODT: case TXT: case YAML:
                return source;
            case MARKDOWN:
                return TextConverter.markdownToText(source);
            case HTML:
                return TextConverter.htmlToText(source);
            case CSV:
                return TextConverter.csvToTextTable(TextConverter.parseCsv(source));
            case TSV:
                return TextConverter.tsvToTextTable(source);
            case JSON:
                return TextConverter.jsonToPrettyText(source);
            case XML:
                return TextConverter.xmlToText(source);
            case SRT:
                return SubtitleKit.srtToText(source);
            case VTT:
                return SubtitleKit.vttToText(source);
            default:
                throw new IOException("TXT 本身已是纯文本，无需再转换：" + item.name);
        }
    }

    /** 14: standalone styled HTML pages. */
    private String convertToHtmlPage(SelectedItem item, String source) throws IOException {
        String title = safeBaseName(item.name);
        switch (item.sourceFormat) {
            case TXT: case PDF: case DOCX: case EPUB: case ODT: case YAML:
                return DocumentKit.html(source, title);
            case MARKDOWN:
                return TextConverter.markdownToHtml(source, title);
            case CSV:
                return TextConverter.csvToHtmlTablePage(
                        TextConverter.parseCsv(source), title);
            case TSV:
                return TextConverter.tsvToHtmlTablePage(source, title);
            case JSON:
                return TextConverter.jsonToHtmlView(source, title);
            default:
                throw new IOException(
                        "HTML 输出接受 Markdown/CSV/TSV/JSON，不支持当前文件类型：" + item.name);
        }
    }

    /** 15: tabular CSV output. */
    private String convertToCsvText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case JSON:
                return TextConverter.jsonToCsv(source);
            case MARKDOWN:
                return TextConverter.markdownTableToCsv(source);
            case TSV:
                return TextConverter.tsvToCsv(source);
            case YAML:
                return TextConverter.yamlToCsv(source);
            default:
                throw new IOException(
                        "CSV 输出接受 JSON/Markdown 表格/TSV/YAML，不支持当前文件类型：" + item.name);
        }
    }

    /** 16: JSON structures. */
    private String convertToJsonText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case JSON: return TextConverter.jsonToPrettyText(source);
            case CSV:
                return TextConverter.csvToJson(TextConverter.parseCsv(source));
            case MARKDOWN:
                return TextConverter.markdownTableToJson(source);
            case TSV:
                return TextConverter.tsvToJson(source);
            case YAML:
                return TextConverter.yamlToJson(source);
            case XML:
                return TextConverter.xmlToJson(source);
            case SRT:
                return SubtitleKit.srtToJson(source);
            case VTT:
                return SubtitleKit.vttToJson(source);
            default:
                throw new IOException(
                        "JSON 输出接受 CSV/TSV/Markdown 表格/YAML/XML/字幕，不支持当前文件类型："
                                + item.name);
        }
    }

    /** 17: YAML output. */
    private String convertToYamlText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case JSON:
                return TextConverter.jsonToYaml(source);
            case CSV:
                return TextConverter.csvToYaml(TextConverter.parseCsv(source));
            case TSV:
                return TextConverter.tsvToYaml(source);
            case MARKDOWN:
                return TextConverter.markdownTableToYaml(source);
            default:
                throw new IOException(
                        "YAML 输出接受 JSON/CSV/TSV/Markdown 表格，不支持当前文件类型：" + item.name);
        }
    }

    /** 18: XML output. */
    private String convertToXmlText(SelectedItem item, String source) throws IOException {
        String rootName = safeBaseName(item.name);
        switch (item.sourceFormat) {
            case JSON:
                return TextConverter.jsonToXml(source, rootName);
            case YAML:
                return TextConverter.yamlToXml(source, rootName);
            case CSV:
                return TextConverter.csvToXml(TextConverter.parseCsv(source), rootName);
            case TSV:
                return TextConverter.tsvToXml(source, rootName);
            case MARKDOWN:
                return TextConverter.markdownTableToXml(source, rootName);
            default:
                throw new IOException(
                        "XML 输出接受 JSON/YAML/CSV/TSV/Markdown 表格，不支持当前文件类型："
                                + item.name);
        }
    }

    /** 19: Markdown table output. */
    private String convertToMarkdownText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case TXT: case PDF: case DOCX: case EPUB: case ODT:
                return source;
            case HTML: return TextConverter.htmlToText(source);
            case CSV:
                return TextConverter.csvToMarkdown(TextConverter.parseCsv(source));
            case TSV:
                return TextConverter.tsvToMarkdown(source);
            case JSON:
                return TextConverter.jsonToMarkdown(source);
            case YAML:
                return TextConverter.yamlToMarkdown(source);
            default:
                throw new IOException(
                        "Markdown 输出接受 CSV/TSV/JSON/YAML 表格数据，不支持当前文件类型："
                                + item.name);
        }
    }

    /** 20: TSV output. */
    private String convertToTsvText(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case CSV:
                return TextConverter.csvToTsv(TextConverter.parseCsv(source));
            case MARKDOWN:
                return TextConverter.markdownTableToTsv(source);
            case JSON:
                return TextConverter.jsonToTsv(source);
            case YAML:
                return TextConverter.yamlToTsv(source);
            default:
                throw new IOException(
                        "TSV 输出接受 CSV/Markdown 表格/JSON/YAML，不支持当前文件类型："
                                + item.name);
        }
    }

    /** Vector text PDF: no full-page bitmap and no lossy JPEG text rendering. */
    private ConversionResult textToPdfDocument(SelectedItem item, String source,
                                               int quality, boolean qualityTouched)
            throws Exception {
        String text = plainTextProjection(item, source);
        checkCancelled();
        Paint body = new Paint(Paint.ANTI_ALIAS_FLAG);
        body.setTextSize(11f);
        body.setColor(0xFF20212A);
        List<TextPager.Page> pages = TextPager.paginate(text, body::measureText,
                TextPager.A4_WIDTH, TextPager.A4_HEIGHT,
                56f, 60f, 50f, 11f, 1.42f, 2000, 24f);
        ensureCacheCapacity(Math.max(8L * 1024 * 1024, text.length() * 8L));
        File output = cacheFile(".pdf");
        Paint footer = new Paint(Paint.ANTI_ALIAS_FLAG);
        footer.setTextSize(8f); footer.setColor(0xFF686A75);
        footer.setTextAlign(Paint.Align.CENTER);
        android.graphics.pdf.PdfDocument pdf = new android.graphics.pdf.PdfDocument();
        try {
            for (int p = 0; p < pages.size(); p++) {
                checkCancelled();
                android.graphics.pdf.PdfDocument.Page page = pdf.startPage(
                        new android.graphics.pdf.PdfDocument.PageInfo.Builder(595, 842, p + 1).create());
                Canvas canvas = page.getCanvas();
                List<String> lines = pages.get(p).lines;
                for (int i = 0; i < lines.size(); i++) {
                    canvas.drawText(lines.get(i), 56f, 60f + 11f * 1.42f * (i + 0.82f), body);
                }
                canvas.drawText("第 " + (p + 1) + " / " + pages.size() + " 页", 297.5f, 816f, footer);
                pdf.finishPage(page);
                updateProgress(300 + (int)(600L*(p+1)/pages.size()), "正在排版第 " + (p+1) + " / " + pages.size() + " 页");
            }
            checkCancelled();
            try (OutputStream out = new BufferedOutputStream(new FileOutputStream(output))) { pdf.writeTo(out); }
        } catch (Throwable error) { output.delete(); throw error; }
        finally { pdf.close(); }
        return new ConversionResult(output,"application/pdf",safeBaseName(item.name)+".pdf");
    }

    /** The readable plain-text projection used by the text-to-PDF pipeline. */
    private String plainTextProjection(SelectedItem item, String source) throws IOException {
        switch (item.sourceFormat) {
            case MARKDOWN:
                return TextConverter.markdownToText(source);
            case HTML:
                return TextConverter.htmlToText(source);
            case CSV:
                return TextConverter.csvToTextTable(TextConverter.parseCsv(source));
            case TSV:
                return TextConverter.tsvToTextTable(source);
            case JSON:
                return TextConverter.jsonToPrettyText(source);
            case XML:
                return TextConverter.xmlToText(source);
            case SRT:
                return SubtitleKit.srtToText(source);
            case VTT:
                return SubtitleKit.vttToText(source);
            default:
                return source; // TXT and YAML are already human-readable text.
        }
    }

    /** Batch conversion: every text file becomes one pending output file. */
    private List<PendingBatchFile> textBatchFiles(List<SelectedItem> items, int format,
                                                  int quality, boolean qualityTouched)
            throws Exception {
        List<PendingBatchFile> outputs = new ArrayList<>();
        try {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                updateProgress((int) (i * 900L / items.size()),
                        "批量转换：" + (i + 1) + " / " + items.size());
                ConversionResult single = convertTextDocument(
                        items.get(i), format, quality, qualityTouched);
                outputs.add(new PendingBatchFile(single.file, single.mime, single.fileName));
            }
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        }
        return outputs;
    }

    /** Batch conversion packed into a single ZIP archive. */
    private ConversionResult textBatchToZip(List<SelectedItem> items, int format,
                                            int quality, boolean qualityTouched) throws Exception {
        List<PendingBatchFile> files = textBatchFiles(items, format, quality, qualityTouched);
        try {
            return zipPendingFiles(files,
                    "converted_" + outputSpec(format).shortName.toLowerCase(Locale.ROOT)
                            + "_" + files.size() + "_files.zip");
        } catch (Throwable error) {
            deleteBatchFiles(files);
            throw error;
        }
    }

    /** Simple generated document-style thumbnail for text files. */
    private Bitmap textThumbnail(SourceFormat format) {
        String badge = textFormatBadge(format);
        int side = dp(96);
        Bitmap bitmap = Bitmap.createBitmap(side, side, Bitmap.Config.ARGB_8888);
        try {
            bitmap.eraseColor(0xFFFFFFFF);
            Canvas canvas = new Canvas(bitmap);
            Paint paper = new Paint(Paint.ANTI_ALIAS_FLAG);
            paper.setColor(0xFFF0F1F5);
            float inset = side * 0.14f;
            canvas.drawRoundRect(new RectF(inset, inset * 0.7f, side - inset, side - inset * 0.7f),
                    side * 0.08f, side * 0.08f, paper);
            Paint badgePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
            badgePaint.setColor(0xFF4A5568);
            badgePaint.setTextAlign(Paint.Align.CENTER);
            badgePaint.setFakeBoldText(true);
            badgePaint.setTextSize(side * (badge.length() >= 3 ? 0.26f : 0.36f));
            Paint.FontMetrics metrics = badgePaint.getFontMetrics();
            float y = side / 2f - (metrics.ascent + metrics.descent) / 2f;
            canvas.drawText(badge, side / 2f, y, badgePaint);
        } catch (Throwable ignored) { }
        return bitmap;
    }

    /** True when the current selection is exactly one PDF and the output is a static image format. */
    private boolean isPdfToStaticImagesMode(int format, List<SelectedItem> items) {
        return isStaticOutputFormat(format)
                && items != null
                && items.size() == 1
                && items.get(0).sourceFormat == SourceFormat.PDF;
    }

    /** Opens the PDF just far enough to count pages; returns 0 when the file cannot be read. */
    private int countPdfPagesSafe(Uri uri) {
        ParcelFileDescriptor handle = null;
        try {
            handle = getContentResolver().openFileDescriptor(uri, "r");
            if (handle == null) return 0;
            try (PdfRenderer renderer = new PdfRenderer(handle)) {
                return renderer.getPageCount();
            }
        } catch (Throwable ignored) {
            return 0;
        } finally {
            if (handle != null) {
                try { handle.close(); } catch (Exception ignored) { }
            }
        }
    }

    /**
     * Renders every page of a PDF into an image file. Page target sizes are derived from the
     * resolution setting and a memory-safe pixel cap, mirroring decodeBitmap behaviour.
     */
    private List<PendingBatchFile> renderPdfPages(
            SelectedItem item, int format, int quality, boolean qualityWasTouched,
            int resolutionPosition, int customWidth, int customHeight) throws Exception {
        OutputSpec spec = outputSpec(format);
        List<PendingBatchFile> outputs = new ArrayList<>();
        updateProgress(2, "正在打开 PDF……");
        checkCancelled();
        ParcelFileDescriptor handle = getContentResolver().openFileDescriptor(item.uri, "r");
        if (handle == null) throw new IOException("无法打开 PDF 文件");
        try (PdfRenderer renderer = new PdfRenderer(handle)) {
            int pageCount = renderer.getPageCount();
            if (pageCount <= 0) throw new IOException("这个 PDF 没有页面");
            ensureCacheCapacity(estimatedStaticOutputBytes(format, 1600, 1600));
            long pixelCap = memorySafePixelCap();
            String base = safeBaseName(item.name);
            for (int i = 0; i < pageCount; i++) {
                checkCancelled();
                try (PdfRenderer.Page page = renderer.openPage(i)) {
                    int pageWidth = page.getWidth();
                    int pageHeight = page.getHeight();
                    int[] target = pdfRenderTargetSize(
                            pageWidth, pageHeight, resolutionPosition,
                            customWidth, customHeight, pixelCap);
                    Bitmap bitmap = Bitmap.createBitmap(
                            target[0], target[1], Bitmap.Config.ARGB_8888);
                    try {
                        bitmap.eraseColor(0xFFFFFFFF);
                        page.render(bitmap, null, null,
                                PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY);
                        checkCancelled();
                        File output = cacheFile(spec.extension);
                        try (OutputStream out = new BufferedOutputStream(
                                new FileOutputStream(output), 256 * 1024)) {
                            int effectiveQuality = resolvedImageQuality(
                                    item, bitmap, format, quality, qualityWasTouched);
                            encodeBitmap(bitmap, format, effectiveQuality, out);
                        }
                        if (output.length() == 0) {
                            throw new IOException("渲染第 " + (i + 1) + " 页失败");
                        }
                        String displayName = pageCount == 1
                                ? base + "_converted" + spec.extension
                                : base + "_page_" + (i + 1) + spec.extension;
                        outputs.add(new PendingBatchFile(output, spec.mime, displayName));
                    } finally {
                        bitmap.recycle();
                    }
                }
                updateProgress((int) ((i + 1) * 1000L / pageCount),
                        "正在渲染页面：" + (i + 1) + " / " + pageCount);
            }
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        } finally {
            try { handle.close(); } catch (Exception ignored) { }
        }
        return outputs;
    }

    /** Target pixel size for one rendered PDF page, honouring the resolution setting. */
    private static int[] pdfRenderTargetSize(
            int pageWidth, int pageHeight, int resolutionPosition,
            int customWidth, int customHeight, long pixelCap) {
        if (pageWidth <= 0 || pageHeight <= 0) {
            return new int[]{Math.max(1, pageWidth), Math.max(1, pageHeight)};
        }
        double scale;
        switch (resolutionPosition) {
            case 0: // 智能推荐：2 倍页面点阵，最多 2000 像素长边
                scale = 2.0;
                scale = Math.min(scale, 2000.0 / Math.max(pageWidth, pageHeight));
                break;
            case 1: // 保持原始：页面点阵 1:1
                scale = 1.0;
                break;
            default: { // 限定边界框，允许放大以填满
                int boxWidth;
                int boxHeight;
                switch (resolutionPosition) {
                    case 2: boxWidth = 640; boxHeight = 480; break;
                    case 3: boxWidth = 1280; boxHeight = 720; break;
                    case 4: boxWidth = 1920; boxHeight = 1080; break;
                    case 5: boxWidth = 2560; boxHeight = 1440; break;
                    case 6: boxWidth = 3840; boxHeight = 2160; break;
                    default:
                        boxWidth = clamp(customWidth, 16, 8192);
                        boxHeight = clamp(customHeight, 16, 8192);
                        break;
                }
                scale = Math.min(boxWidth / (double) pageWidth,
                        boxHeight / (double) pageHeight);
                break;
            }
        }
        int width = Math.max(1, (int) Math.round(pageWidth * scale));
        int height = Math.max(1, (int) Math.round(pageHeight * scale));
        long pixels = (long) width * height;
        if (pixels > pixelCap) {
            double shrink = Math.sqrt(pixelCap / (double) pixels);
            width = Math.max(1, (int) Math.floor(width * shrink));
            height = Math.max(1, (int) Math.floor(height * shrink));
        }
        return new int[]{width, height};
    }

    private static long memorySafePixelCap() {
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long availableMemory = Math.max(1L, maxMemory - usedMemory);
        return Math.max(65_536L,
                Math.min(maxMemory / 16L, availableMemory / 16L));
    }

    /** Combines the selected images into a single multi-page PDF document. */
    private ConversionResult imagesToPdf(
            List<SelectedItem> items, int quality, boolean qualityWasTouched) throws Exception {
        ensureCacheCapacity(saturatingAdd(
                8L * 1024 * 1024, saturatingMultiply(2L * 1024 * 1024, items.size())));
        File output = cacheFile(".pdf");
        try (SimplePdfWriter pdf = new SimplePdfWriter(output)) {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                updateProgress((int) (i * 800L / items.size()),
                        "正在处理图片：" + (i + 1) + " / " + items.size());
                int[] bounds = selectedBounds(0, 0, false);
                Bitmap bitmap = decodeBitmap(item.uri, bounds[0], bounds[1], 80_000_000L);
                checkCancelled();
                if (bitmap == null) throw new IOException("无法解码图片：" + item.name);
                try {
                    Bitmap flat = flatten(bitmap, 0xFFFFFFFF);
                    boolean borrowed = flat != bitmap;
                    try {
                        int effectiveQuality = resolvedImageQuality(
                                item, flat, 0, quality, qualityWasTouched);
                        ByteArrayOutputStream bytes = new ByteArrayOutputStream(256 * 1024);
                        updateProgress((int) ((i + 40) * 800L / items.size()),
                                "正在压缩页面图片……");
                        boolean success = flat.compress(
                                Bitmap.CompressFormat.JPEG, effectiveQuality, bytes);
                        if (!success || bytes.size() == 0) {
                            throw new IOException("页面图片编码失败：" + item.name);
                        }
                        pdf.writePage(bytes.toByteArray(),
                                flat.getWidth(), flat.getHeight());
                    } finally {
                        if (borrowed) flat.recycle();
                    }
                } finally {
                    bitmap.recycle();
                }
            }
            checkCancelled();
            updateProgress(880, "正在写入 PDF 收尾数据……");
            pdf.finish();
        }
        checkCancelled();
        updateProgress(1000, "PDF 生成完成");
        String name = items.size() == 1
                ? safeBaseName(items.get(0).name) + ".pdf"
                : "images_to_pdf.pdf";
        return new ConversionResult(output, "application/pdf", name);
    }

    /** Builds the square PNG frames for one image, in ascending icon sizes. */
    private List<IcoWriter.Frame> icoFramesFor(SelectedItem item) throws Exception {
        int[] bounds = selectedBounds(0, 0, false);
        Bitmap bitmap = decodeBitmap(item.uri, bounds[0], bounds[1], 40_000_000L);
        checkCancelled();
        if (bitmap == null) throw new IOException("无法解码图片：" + item.name);
        try {
            int side = Math.min(bitmap.getWidth(), bitmap.getHeight());
            Bitmap square = Bitmap.createBitmap(side, side, Bitmap.Config.ARGB_8888);
            try {
                Canvas canvas = new Canvas(square);
                Paint paint = new Paint(Paint.FILTER_BITMAP_FLAG);
                canvas.drawBitmap(bitmap,
                        (side - bitmap.getWidth()) / 2f,
                        (side - bitmap.getHeight()) / 2f, paint);
            } catch (Throwable error) {
                square.recycle();
                throw error;
            }
            List<IcoWriter.Frame> frames = new ArrayList<>();
            try {
                int[] sizes = {16, 24, 32, 48, 64, 96, 128, 256};
                for (int size : sizes) {
                    if (size > side && !(frames.isEmpty() && size == 16)) continue;
                    checkCancelled();
                    Bitmap scaled = Bitmap.createScaledBitmap(square, size, size, true);
                    try {
                        ByteArrayOutputStream bytes = new ByteArrayOutputStream(64 * 1024);
                        boolean success = scaled.compress(
                                Bitmap.CompressFormat.PNG, 100, bytes);
                        if (!success || bytes.size() == 0) {
                            throw new IOException("PNG 帧编码失败：" + item.name);
                        }
                        frames.add(new IcoWriter.Frame(bytes.toByteArray(), size));
                    } finally {
                        if (scaled != square) scaled.recycle();
                    }
                }
            } finally {
                square.recycle();
            }
            if (frames.isEmpty()) {
                throw new IOException("图片太小，无法生成图标：" + item.name);
            }
            return frames;
        } finally {
            bitmap.recycle();
        }
    }

    private ConversionResult imageToIco(SelectedItem item) throws Exception {
        updateProgress(30, "正在读取图片……");
        checkCancelled();
        ensureCacheCapacity(4L * 1024 * 1024);
        List<IcoWriter.Frame> frames = icoFramesFor(item);
        checkCancelled();
        updateProgress(80, "正在写入 ICO……");
        File output = cacheFile(".ico");
        IcoWriter.write(output, frames);
        updateProgress(1000, "图标生成完成");
        return new ConversionResult(output, "image/x-icon",
                safeBaseName(item.name) + "_converted.ico");
    }

    private BatchConversionResult imagesToIcoBatch(List<SelectedItem> items) throws Exception {
        List<PendingBatchFile> outputs = new ArrayList<>();
        Set<String> usedNames = new HashSet<>();
        try {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                updateProgress((int) (i * 1000L / items.size()),
                        "正在生成图标：" + (i + 1) + " / " + items.size());
                File output = cacheFile(".ico");
                IcoWriter.write(output, icoFramesFor(item));
                if (output.length() == 0) throw new IOException("输出文件为空：" + item.name);
                String displayName = uniqueEntryName(
                        safeBaseName(item.name) + "_converted.ico", usedNames);
                outputs.add(new PendingBatchFile(output, "image/x-icon", displayName));
            }
            return new BatchConversionResult(outputs);
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        }
    }

    private ConversionResult imagesToIcoZip(List<SelectedItem> items) throws Exception {
        List<PendingBatchFile> outputs = new ArrayList<>();
        Set<String> usedNames = new HashSet<>();
        try {
            for (int i = 0; i < items.size(); i++) {
                checkCancelled();
                SelectedItem item = items.get(i);
                updateProgress((int) (i * 900L / items.size()),
                        "正在生成图标：" + (i + 1) + " / " + items.size());
                File output = cacheFile(".ico");
                IcoWriter.write(output, icoFramesFor(item));
                if (output.length() == 0) throw new IOException("输出文件为空：" + item.name);
                String displayName = uniqueEntryName(
                        safeBaseName(item.name) + "_converted.ico", usedNames);
                outputs.add(new PendingBatchFile(output, "image/x-icon", displayName));
            }
            checkCancelled();
            updateProgress(950, "正在打包 ZIP……");
            return zipPendingFiles(outputs, "converted_ico_" + items.size() + "_files.zip");
        } catch (Throwable error) {
            deleteBatchFiles(outputs);
            throw error;
        }
    }

    /** Packs finished conversion files into one ZIP and deletes the loose files. */
    private ConversionResult zipPendingFiles(
            List<PendingBatchFile> files, String fileName) throws Exception {
        File output = cacheFile(".zip");
        try (ZipOutputStream zip = new ZipOutputStream(
                new BufferedOutputStream(new FileOutputStream(output), 256 * 1024))) {
            zip.setLevel(Deflater.BEST_SPEED);
            for (PendingBatchFile file : files) {
                checkCancelled();
                zip.putNextEntry(new ZipEntry(file.fileName));
                try (InputStream in = new BufferedInputStream(
                        new FileInputStream(file.file))) {
                    byte[] buffer = new byte[64 * 1024];
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        zip.write(buffer, 0, read);
                    }
                }
                zip.closeEntry();
            }
        } catch (Throwable error) {
            deleteBatchFiles(files);
            throw error;
        }
        deleteBatchFiles(files);
        checkCancelled();
        if (output.length() == 0) throw new IOException("ZIP 生成失败");
        return new ConversionResult(output, "application/zip", fileName);
    }

    private void encodeBitmap(Bitmap bitmap, int format, int quality, OutputStream out)
            throws IOException {
        if(format>=29&&format<=34){ExtraImageFormats.write(bitmap,format,out);return;}
        boolean success;
        if (format == 0) {
            Bitmap flat = flatten(bitmap, 0xFFFFFFFF);
            try { success = flat.compress(Bitmap.CompressFormat.JPEG, quality, out); }
            finally { if (flat != bitmap) flat.recycle(); }
        } else if (format == 1) {
            success = bitmap.compress(Bitmap.CompressFormat.PNG, 100, out);
        } else if (format == 2) {
            Bitmap flat = flatten(bitmap, 0xFFFFFFFF);
            try { writeBmp(flat, out); }
            finally { if (flat != bitmap) flat.recycle(); }
            success = true;
        } else if (format == 7) {
            Bitmap.CompressFormat webp = Build.VERSION.SDK_INT >= 30
                    ? Bitmap.CompressFormat.WEBP_LOSSY
                    : Bitmap.CompressFormat.WEBP;
            success = bitmap.compress(webp, quality, out);
        } else if (format == 8) {
            Bitmap.CompressFormat webp = Build.VERSION.SDK_INT >= 30
                    ? Bitmap.CompressFormat.WEBP_LOSSLESS
                    : Bitmap.CompressFormat.WEBP;
            success = bitmap.compress(webp, 100, out);
        } else {
            throw new IOException("不支持的静态输出格式");
        }
        if (!success) throw new IOException("图片编码失败");
    }

    private int resolvedImageQuality(
            SelectedItem item, Bitmap bitmap, int format,
            int requestedQuality, boolean qualityWasTouched) throws CancelledException {
        if ((format != 0 && format != 7)
                || qualityWasTouched || !isSmartResolution()) {
            return requestedQuality;
        }

        ImageProfile profile = analyzeImage(bitmap);
        return qualityForProfile(item, profile, format, (long)bitmap.getWidth()*bitmap.getHeight());
    }

    private int qualityForProfile(SelectedItem item,ImageProfile profile,int format,long pixelCount) {
        int quality = format == 0 ? 86 : 80;
        if (profile.edgeStrength >= 30) quality += 7;
        else if (profile.edgeStrength >= 18) quality += 5;
        else if (profile.edgeStrength >= 10) quality += 3;
        else if (profile.edgeStrength >= 5) quality += 1;
        if (profile.contrast >= 70) quality += 1;

        if (item != null && item.size > 0
                && (item.sourceFormat == SourceFormat.JPEG
                || item.sourceFormat == SourceFormat.WEBP
                || item.sourceFormat == SourceFormat.HEIC)) {
            long pixels = Math.max(1L, pixelCount);
            double compressedBytesPerPixel = item.size / (double) pixels;
            if (compressedBytesPerPixel >= 1.0) quality += 1;
            else if (compressedBytesPerPixel < 0.12) quality -= 1;
        }

        return format == 0 ? clamp(quality, 84, 95) : clamp(quality, 78, 92);
    }

    private ImageProfile analyzeImage(Bitmap bitmap) throws CancelledException {
        checkCancelled();
        int width = Math.max(1, Math.min(72, bitmap.getWidth()));
        int height = Math.max(1, Math.min(72, bitmap.getHeight()));
        Bitmap sample = bitmap;
        if (width != bitmap.getWidth() || height != bitmap.getHeight()) {
            sample = Bitmap.createScaledBitmap(bitmap, width, height, false);
        }
        int[] colors = new int[width * height];
        try {
            sample.getPixels(colors, 0, width, 0, 0, width, height);
        } finally {
            if (sample != bitmap) sample.recycle();
        }
        checkCancelled();

        long lumaSum = 0;
        long lumaSquaredSum = 0;
        long edgeSum = 0;
        long edgeCount = 0;
        int previousRowOffset = -1;
        for (int y = 0; y < height; y++) {
            int rowOffset = y * width;
            int previousLuma = -1;
            for (int x = 0; x < width; x++) {
                int color = colors[rowOffset + x];
                int luma = (77 * ((color >>> 16) & 0xFF)
                        + 150 * ((color >>> 8) & 0xFF)
                        + 29 * (color & 0xFF)) >>> 8;
                lumaSum += luma;
                lumaSquaredSum += (long) luma * luma;
                if (previousLuma >= 0) {
                    edgeSum += Math.abs(luma - previousLuma);
                    edgeCount++;
                }
                if (previousRowOffset >= 0) {
                    int above = colors[previousRowOffset + x];
                    int aboveLuma = (77 * ((above >>> 16) & 0xFF)
                            + 150 * ((above >>> 8) & 0xFF)
                            + 29 * (above & 0xFF)) >>> 8;
                    edgeSum += Math.abs(luma - aboveLuma);
                    edgeCount++;
                }
                previousLuma = luma;
            }
            previousRowOffset = rowOffset;
        }
        double count = Math.max(1, colors.length);
        double mean = lumaSum / count;
        double variance = Math.max(0, lumaSquaredSum / count - mean * mean);
        return new ImageProfile(
                edgeSum / (double) Math.max(1, edgeCount),
                Math.sqrt(variance));
    }

    private boolean isSmartResolution() {
        ConversionSettings settings = runningSettings;
        return settings != null && settings.resolutionPosition == 0;
    }

    private AnimationEdits currentAnimationEdits() {
        ConversionSettings settings = runningSettings;
        if (settings != null && settings.edits != null) return settings.edits;
        return animationEdits == null ? freshAnimationEdits() : animationEdits;
    }

    private int[] smartVideoGifBounds(
            List<SelectedItem> items,
            List<VideoFrameDecoder.Info> infos,
            List<Long> startsUs,
            List<Long> endsUs,
            long outputFrames) {
        double weightedQuality = 0;
        double weightSum = 0;
        long onePassDurationUs = 0;
        for (int i = 0; i < infos.size(); i++) {
            VideoFrameDecoder.Info info = infos.get(i);
            long durationUs = Math.max(1L, endsUs.get(i) - startsUs.get(i));
            onePassDurationUs = saturatingAdd(onePassDurationUs, durationUs);
            long pixels = Math.max(1L,
                    (long) info.orientedWidth() * info.orientedHeight());
            int sourceFps = info.frameRate > 0 ? clamp(info.frameRate, 1, 240) : 30;
            double bitrate = info.bitrate;
            if (bitrate <= 0 && i < items.size() && items.get(i).size > 0
                    && info.durationUs > 0) {
                bitrate = items.get(i).size * 8_000_000.0 / info.durationUs;
            }
            double bitsPerPixelFrame = bitrate > 0
                    ? bitrate / (pixels * (double) sourceFps)
                    : 0.065;
            weightedQuality += Math.min(0.20, bitsPerPixelFrame) * durationUs;
            weightSum += durationUs;
        }
        double quality = weightSum > 0 ? weightedQuality / weightSum : 0.065;
        double onePassSeconds = onePassDurationUs / 1_000_000.0;
        long maxMemory = Runtime.getRuntime().maxMemory();

        int width;
        int height;
        if (quality < 0.035 || outputFrames > 300 || onePassSeconds > 20) {
            width = 480;
            height = 360;
        } else if (quality >= 0.075 && outputFrames <= 90
                && onePassSeconds <= 8 && maxMemory >= 192L * 1024 * 1024) {
            width = 960;
            height = 720;
        } else if (quality >= 0.052 && outputFrames <= 180) {
            width = 720;
            height = 540;
        } else {
            width = 640;
            height = 480;
        }
        return gifMemorySafeBounds(width, height);
    }

    private int[] smartImageGifBounds(
            Bitmap firstFrame, int frameCount, int fps) throws CancelledException {
        ImageProfile profile = analyzeImage(firstFrame);
        long timelineLoad = (long) frameCount * Math.max(1, fps);
        long maxMemory = Runtime.getRuntime().maxMemory();
        int width;
        int height;
        if (frameCount > 180 || timelineLoad > 3600 || profile.edgeStrength < 4) {
            width = 480;
            height = 360;
        } else if (frameCount <= 60 && profile.edgeStrength >= 14
                && profile.contrast >= 35 && maxMemory >= 192L * 1024 * 1024) {
            width = 960;
            height = 720;
        } else {
            width = 640;
            height = 480;
        }
        return gifMemorySafeBounds(width, height);
    }

    private int[] smartAnimatedGifBounds(
            int sourceWidth, int sourceHeight, int durationMs,
            int frameCount, long sourceBytes) {
        long pixels = Math.max(1L, (long) sourceWidth * sourceHeight);
        double bytesPerPixelFrame = sourceBytes > 0
                ? sourceBytes / (double) Math.max(1L, pixels * Math.max(1L, frameCount))
                : 0.12;
        int width;
        int height;
        if (frameCount > 240 || durationMs > 20_000 || bytesPerPixelFrame < 0.045) {
            width = 480;
            height = 360;
        } else if (frameCount <= 90 && durationMs <= 8_000
                && bytesPerPixelFrame >= 0.10
                && Runtime.getRuntime().maxMemory() >= 192L * 1024 * 1024) {
            width = 960;
            height = 720;
        } else {
            width = 640;
            height = 480;
        }
        return gifMemorySafeBounds(width, height);
    }

    private int[] gifMemorySafeBounds(int requestedWidth, int requestedHeight) {
        int width = Math.max(1, Math.min(4096, requestedWidth));
        int height = Math.max(1, Math.min(4096, requestedHeight));
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long availableMemory = Math.max(1L, maxMemory - usedMemory);
        long memorySafePixels = Math.max(320L * 240L,
                Math.min(4096L * 4096L,
                        Math.min(maxMemory / 32L, availableMemory / 20L)));
        long requestedPixels = (long) width * height;
        if (requestedPixels > memorySafePixels) {
            double scale = Math.sqrt(memorySafePixels / (double) requestedPixels);
            width = Math.max(1, (int) Math.floor(width * scale));
            height = Math.max(1, (int) Math.floor(height * scale));
        }
        return new int[]{width, height};
    }

    private ConversionResult gifToGif(
            Uri uri, String name, int requestedFps, int frameLimit,
            int repetitions, int reverseMode) throws Exception {
        File output = cacheFile(".gif");
        AnimationEdits edits = currentAnimationEdits();
        GifDrawable gif = null;
        Bitmap frameBitmap = null;
        Bitmap sourceBitmap = null;
        try {
            gif = new GifDrawable(getContentResolver(), uri);
            gif.stop();
            int sourceWidth = Math.max(1, gif.getIntrinsicWidth());
            int sourceHeight = Math.max(1, gif.getIntrinsicHeight());
            int durationMs = Math.max(1, gif.getDuration());
            int clipStartMs = Math.min(durationMs - 1,
                    Math.max(0, (int) Math.round(edits.trimStartSeconds * 1000.0)));
            int clipEndMs = edits.trimDurationSeconds <= 0.0
                    ? durationMs
                    : Math.min(durationMs, clipStartMs + Math.max(1,
                            (int) Math.round(edits.trimDurationSeconds * 1000.0)));
            double clipStartSeconds = clipStartMs / 1000.0;
            double clipEndSeconds = clipEndMs / 1000.0;
            double keptDurationSeconds = edits.keptDurationSeconds(
                    clipStartSeconds, clipEndSeconds);
            if (keptDurationSeconds <= 0.0005) {
                throw new IOException("分割删除后没有可用 GIF 片段");
            }
            double outputDurationSeconds = keptDurationSeconds / edits.speed;
            GifPlaybackPlan plan = new GifPlaybackPlan(outputDurationSeconds,
                    requestedFps, frameLimit, repetitions, reverseMode);
            int frameCount = plan.totalFrames;
            int[] editedSourceSize = FrameEditor.editedSize(
                    sourceWidth, sourceHeight, edits);
            int[] requested = isSmartResolution()
                    ? smartAnimatedGifBounds(
                            editedSourceSize[0], editedSourceSize[1],
                            (int) Math.max(1, Math.min(Integer.MAX_VALUE, Math.round(plan.totalSeconds * 1000.0))),
                            frameCount,
                            queryFileSize(uri))
                    : selectedBounds(
                            editedSourceSize[0], editedSourceSize[1], true);
            int[] size = fitSize(
                    editedSourceSize[0], editedSourceSize[1],
                    requested[0], requested[1], true);
            double actualFps = plan.actualFps;
            int delayMs = Math.max(10, (int) Math.round(1000.0 / actualFps));
            boolean cacheFrames = plan.passes > 1 || reverseMode != 0;
            long cacheBytes = cacheFrames ? (long) size[0] * size[1] * plan.framesPerPass : 0;
            ensureCacheCapacity(saturatingAdd(estimatedGifOutputBytes(size[0], size[1], frameCount), cacheBytes));
            frameBitmap = Bitmap.createBitmap(size[0], size[1], Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(frameBitmap);
            Canvas sourceCanvas = null;
            Paint editPaint = FrameEditor.createPaint(edits);
            if (edits.hasVisualEdits()) {
                int[] decodeBounds = FrameEditor.decodeBounds(
                        sourceWidth, sourceHeight, size[0], size[1], edits);
                sourceBitmap = Bitmap.createBitmap(
                        decodeBounds[0], decodeBounds[1], Bitmap.Config.ARGB_8888);
                sourceCanvas = new Canvas(sourceBitmap);
                gif.setBounds(0, 0, sourceBitmap.getWidth(), sourceBitmap.getHeight());
            } else {
                int[] drawSize = fitSize(
                        sourceWidth, sourceHeight, size[0], size[1], true);
                int left = (size[0] - drawSize[0]) / 2;
                int top = (size[1] - drawSize[1]) / 2;
                gif.setBounds(left, top, left + drawSize[0], top + drawSize[1]);
            }
            int[] pixels = new int[size[0] * size[1]];
            byte[] indexes = new byte[size[0] * size[1]];
            try (OutputStream out = new BufferedOutputStream(
                         new FileOutputStream(output), 256 * 1024);
                 FastGifEncoder encoder = new FastGifEncoder(
                         out, size[0], size[1], currentGifLoopCount(), this::isCancellationRequested)) {
                SeamlessGifWriter gifWriter = new SeamlessGifWriter(encoder, delayMs);
                File frameCache = new File(getCacheDir(), "gif_edit_" + System.nanoTime() + ".cache");
                try (IndexedFrameStore store = cacheFrames
                        ? new IndexedFrameStore(frameCache, encoder.pixelCount(), this::isCancellationRequested) : null) {
                    boolean[] boundaries = new boolean[plan.framesPerPass];
                    double previousSourceSecond = -1.0;
                    for (int i = 0; i < plan.framesPerPass; i++) {
                        checkCancelled();
                        double keptOffset = i * keptDurationSeconds / plan.framesPerPass;
                        double sourceSecond = edits.sourceSecondAtKeptOffset(clipStartSeconds, clipEndSeconds, keptOffset);
                        boundaries[i] = previousSourceSecond >= 0
                                && Math.abs(sourceSecond - previousSourceSecond) > Math.max(.05, edits.speed * 2.5 / actualFps);
                        previousSourceSecond = sourceSecond;
                        int gifTimeMs = Math.min(durationMs - 1, Math.max(0,(int)Math.round(sourceSecond * 1000)));
                        // seekTo() queues asynchronous work; export must wait for the requested frame.
                        gif.seekToBlocking(gifTimeMs);
                        checkCancelled();
                        if (sourceBitmap != null && sourceCanvas != null) {
                            sourceCanvas.drawColor(0xFFFFFFFF); gif.draw(sourceCanvas);
                            FrameEditor.drawBitmap(canvas, sourceBitmap, 0xFFFFFFFF, edits, editPaint);
                        } else { canvas.drawColor(0xFFFFFFFF); gif.draw(canvas); }
                        frameBitmap.getPixels(pixels,0,size[0],0,0,size[0],size[1]);
                        encoder.indexPixels(pixels,indexes);
                        if (store != null) store.add(indexes);
                        else {if(boundaries[i])gifWriter.markSegmentBoundary();gifWriter.offer(indexes);}
                        updateProgress((int)((i+1L)*(cacheFrames?450:990)/plan.framesPerPass),
                                "GIF 帧处理："+(i+1)+"/"+plan.framesPerPass+" · "+size[0]+"×"+size[1]);
                    }
                    if (store != null) for (int pass=1;pass<=plan.passes;pass++) {
                        boolean reverse=GifPlaybackPlan.reversed(pass,reverseMode);
                        if(pass>1)gifWriter.markSegmentBoundary();
                        for(int position=0;position<plan.framesPerPass;position++) {
                            checkCancelled();int index=plan.frameIndex(pass,position,reverseMode);
                            if(position>0 && boundaries[reverse?index+1:index])gifWriter.markSegmentBoundary();
                            store.read(index,indexes);gifWriter.offer(indexes);
                            long written=(long)(pass-1)*plan.framesPerPass+position+1;
                            updateProgress(450+(int)(written*540/plan.totalFrames),
                                    String.format(Locale.CHINA,"第 %d/%d 轮%s · %.2f FPS",pass,plan.passes,reverse?"倒放":"正放",actualFps));
                        }
                    }
                }
                checkCancelled();
                gifWriter.finishFrames(currentGifLoopCount() == 0);
                encoder.finish();
            }
        } finally {
            if (sourceBitmap != null) sourceBitmap.recycle();
            if (frameBitmap != null) frameBitmap.recycle();
            if (gif != null) gif.recycle();
        }
        checkCancelled();
        if (output.length() == 0) throw new IOException("GIF 生成失败");
        return new ConversionResult(output, "image/gif",
                safeBaseName(name) + "_converted.gif");
    }

    private Bitmap decodeBitmap(Uri uri, int maxWidth, int maxHeight, long maxPixels)
            throws IOException {
        String extraKind=ExtraImageFormats.kind(this,uri);
        if(!extraKind.isEmpty())return ExtraImageFormats.decode(this,uri,extraKind,maxWidth,maxHeight,Math.min(maxPixels,memorySafePixelCap()));
        ImageDecoder.Source source = ImageDecoder.createSource(getContentResolver(), uri);
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long availableMemory = Math.max(1L, maxMemory - usedMemory);
        long memorySafePixels = Math.max(65_536L,
                Math.min(maxMemory / 12L, availableMemory / 12L));
        final long safeMaxPixels = Math.min(maxPixels, memorySafePixels);
        return ImageDecoder.decodeBitmap(source, (decoder, info, src) -> {
            decoder.setAllocator(ImageDecoder.ALLOCATOR_SOFTWARE);
            int width = info.getSize().getWidth();
            int height = info.getSize().getHeight();
            int[] target = fitSize(width, height, maxWidth, maxHeight, true);
            long pixels = (long) target[0] * target[1];
            if (pixels > safeMaxPixels) {
                double scale = Math.sqrt(safeMaxPixels / (double) pixels);
                target[0] = Math.max(1, (int) Math.floor(target[0] * scale));
                target[1] = Math.max(1, (int) Math.floor(target[1] * scale));
            }
            if (target[0] != width || target[1] != height) {
                decoder.setTargetSize(target[0], target[1]);
            }
        });
    }

    private int[] selectedBounds(int sourceWidth, int sourceHeight, boolean gifSafe) {
        ConversionSettings settings = runningSettings;
        int position = settings != null ? settings.resolutionPosition
                : resolutionSpinner.getSelectedItemPosition();
        int width;
        int height;
        switch (position) {
            case 0:
                if (gifSafe) {
                    width = 640;
                    height = 480;
                } else {
                    width = sourceWidth > 0 ? sourceWidth : 16384;
                    height = sourceHeight > 0 ? sourceHeight : 16384;
                }
                break;
            case 1:
                width = sourceWidth > 0 ? sourceWidth : 16384;
                height = sourceHeight > 0 ? sourceHeight : 16384;
                break;
            case 2: width = 640; height = 480; break;
            case 3: width = 1280; height = 720; break;
            case 4: width = 1920; height = 1080; break;
            case 5: width = 2560; height = 1440; break;
            case 6: width = 3840; height = 2160; break;
            default:
                if (settings != null) {
                    width = settings.customWidth;
                    height = settings.customHeight;
                } else {
                    width = clamp(parseInt(customWidthEdit.getText().toString(), 1280), 16, 8192);
                    height = clamp(parseInt(customHeightEdit.getText().toString(), 720), 16, 8192);
                }
                break;
        }
        if (gifSafe) return gifMemorySafeBounds(width, height);
        return new int[]{Math.max(1, width), Math.max(1, height)};
    }

    private int selectedFps() {
        int[] values = {5, 10, 12, 15, 20, 24, 30, 60};
        int pos = fpsSpinner.getSelectedItemPosition();
        if (pos < values.length) return values[pos];
        return clamp(parseInt(customFpsEdit.getText().toString(), 12), 1, 120);
    }

    private int selectedFrameLimit() {
        int[] values = {300, 600, 1000, 2000, 5000};
        int pos = frameLimitSpinner.getSelectedItemPosition();
        if (pos < values.length) return values[pos];
        return clamp(parseInt(customFrameLimitEdit.getText().toString(), 1000), 1, 10000);
    }

    private int selectedBitrate() {
        int[] values = {0, 2, 4, 8, 12, 20, 40};
        int pos = bitrateSpinner.getSelectedItemPosition();
        int mbps = pos < values.length
                ? values[pos]
                : clamp((int) Math.round(parseDouble(
                        customBitrateEdit.getText().toString(), 8)), 1, 120);
        return mbps == 0 ? 0 : mbps * 1_000_000;
    }

    private int selectedLoops() {
        int[] values = {1, 2, 3, 5, 10};
        int pos = loopSpinner.getSelectedItemPosition();
        if (pos < values.length) return values[pos];
        return clamp(parseInt(customLoopEdit.getText().toString(), 1), 1, 100);
    }

    private int selectedVideoLoops() {
        int[] values = {1, 2, 3, 5, 10};
        int pos = videoLoopSpinner.getSelectedItemPosition();
        if (pos < values.length) return values[pos];
        return clamp(parseInt(customVideoLoopEdit.getText().toString(), 1), 1, 100);
    }

    private int selectedReverseLoop() {
        int[] values = {0, 1, 2, 3, 5, 10};
        int pos = reverseLoopSpinner.getSelectedItemPosition();
        if (pos == 7) return GifPlaybackPlan.REVERSE_ALL;
        if (pos == 8) return GifPlaybackPlan.PING_PONG;
        if (pos < values.length) return values[pos];
        return clamp(parseInt(customReverseLoopEdit.getText().toString(), 0), 0, 100);
    }

    private int currentGifLoopCount() {
        return runningSettings == null ? 0 : runningSettings.gifLoopCount;
    }

    private boolean hasTimedSourceSelected() {
        for (SelectedItem item : selectedItems) {
            if (item.isVideo() || item.sourceFormat == SourceFormat.GIF) return true;
        }
        return false;
    }

    private boolean hasOnlyVideosSelected() {
        return hasOnlyVideos(selectedItems);
    }

    private boolean hasOnlyVideos(List<SelectedItem> items) {
        if (items == null || items.isEmpty()) return false;
        for (SelectedItem item : items) {
            if (!item.isVideo()) return false;
        }
        return true;
    }

    private int[] fitSize(int width, int height, int maxWidth, int maxHeight, boolean noUpscale) {
        if (width <= 0 || height <= 0) return new int[]{maxWidth, maxHeight};
        double scale = Math.min(maxWidth / (double) width, maxHeight / (double) height);
        if (noUpscale) scale = Math.min(1.0, scale);
        return new int[]{
                Math.max(1, (int) Math.round(width * scale)),
                Math.max(1, (int) Math.round(height * scale))
        };
    }

    private Bitmap fitToRequested(Bitmap source, int width, int height, boolean noUpscale) {
        int[] size = fitSize(source.getWidth(), source.getHeight(), width, height, noUpscale);
        if (size[0] == source.getWidth() && size[1] == source.getHeight()) return source;
        return Bitmap.createScaledBitmap(source, size[0], size[1], true);
    }

    private Bitmap fitOnCanvas(Bitmap source, int width, int height, int background) {
        int[] size = fitSize(source.getWidth(), source.getHeight(), width, height, true);
        if (size[0] == source.getWidth() && size[1] == source.getHeight()
                && source.getWidth() == width && source.getHeight() == height
                && !source.hasAlpha()) {
            return source;
        }
        Bitmap result = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(result);
        canvas.drawColor(background);
        float left = (width - size[0]) / 2f;
        float top = (height - size[1]) / 2f;
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.FILTER_BITMAP_FLAG);
        canvas.drawBitmap(source, null,
                new RectF(left, top, left + size[0], top + size[1]), paint);
        return result;
    }

    private Bitmap flatten(Bitmap source, int background) {
        if (!source.hasAlpha()) return source;
        Bitmap result = Bitmap.createBitmap(
                source.getWidth(), source.getHeight(), Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(result);
        canvas.drawColor(background);
        canvas.drawBitmap(source, 0, 0, null);
        return result;
    }

    private Bitmap flattenReplacing(Bitmap source, int background) {
        Bitmap flat = flatten(source, background);
        if (flat != source) source.recycle();
        return flat;
    }

    private void offerGifFrame(
            FastGifEncoder encoder, SeamlessGifWriter gifWriter, Bitmap bitmap,
            int[] pixels, byte[] indexes)
            throws IOException {
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        if (pixels.length < width * height) {
            throw new IOException("GIF 像素缓冲区尺寸不足");
        }
        bitmap.getPixels(pixels, 0, width, 0, 0, width, height);
        encoder.indexPixels(pixels, indexes);
        gifWriter.offer(indexes);
    }

    private void writeBmp(Bitmap bitmap, OutputStream out) throws IOException {
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        int rowStride = ((width * 3) + 3) & ~3;
        int pixelDataSize = rowStride * height;
        int fileSize = 14 + 40 + pixelDataSize;

        out.write('B');
        out.write('M');
        writeLittleEndianInt(out, fileSize);
        writeLittleEndianShort(out, 0);
        writeLittleEndianShort(out, 0);
        writeLittleEndianInt(out, 54);

        writeLittleEndianInt(out, 40);
        writeLittleEndianInt(out, width);
        writeLittleEndianInt(out, height);
        writeLittleEndianShort(out, 1);
        writeLittleEndianShort(out, 24);
        writeLittleEndianInt(out, 0);
        writeLittleEndianInt(out, pixelDataSize);
        writeLittleEndianInt(out, 2835);
        writeLittleEndianInt(out, 2835);
        writeLittleEndianInt(out, 0);
        writeLittleEndianInt(out, 0);

        int[] pixels = new int[width];
        byte[] row = new byte[rowStride];
        for (int y = height - 1; y >= 0; y--) {
            if ((y & 15) == 0 && isCancellationRequested()) {
                throw new InterruptedIOException("转换已取消");
            }
            bitmap.getPixels(pixels, 0, width, 0, y, width, 1);
            int offset = 0;
            for (int x = 0; x < width; x++) {
                int color = pixels[x];
                row[offset++] = (byte) (color & 0xFF);
                row[offset++] = (byte) ((color >> 8) & 0xFF);
                row[offset++] = (byte) ((color >> 16) & 0xFF);
            }
            while (offset < rowStride) row[offset++] = 0;
            out.write(row, 0, rowStride);
        }
    }

    private void writeLittleEndianShort(OutputStream out, int value) throws IOException {
        out.write(value & 0xFF);
        out.write((value >>> 8) & 0xFF);
    }

    private void writeLittleEndianInt(OutputStream out, int value) throws IOException {
        out.write(value & 0xFF);
        out.write((value >>> 8) & 0xFF);
        out.write((value >>> 16) & 0xFF);
        out.write((value >>> 24) & 0xFF);
    }

    private void launchSavePicker(ConversionResult result) {
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(result.mime);
        intent.putExtra(Intent.EXTRA_TITLE, result.fileName);
        startActivityForResult(intent, REQUEST_SAVE);
    }

    private void launchSaveFolderPicker() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);
        startActivityForResult(intent, REQUEST_SAVE_FOLDER);
    }

    private void savePendingBatchToFolder(Uri treeUri) {
        final List<PendingBatchFile> batch = pendingBatchFiles == null
                ? Collections.emptyList() : new ArrayList<>(pendingBatchFiles);
        if (batch.isEmpty()) {
            cleanupPending();
            setBusy(false);
            statusText.setText("没有可保存的批量文件。");
            return;
        }
        cancelRequested = false;
        updateProgress(0, "正在保存批量文件……");
        currentTask = executor.submit(() -> {
            taskRunning = true;
            List<Uri> createdDocuments = new ArrayList<>();
            try {
                Uri parent = DocumentsContract.buildDocumentUriUsingTree(
                        treeUri, DocumentsContract.getTreeDocumentId(treeUri));
                long totalBytes = 0;
                for (PendingBatchFile file : batch) totalBytes += Math.max(1, file.file.length());
                long copiedAll = 0;
                byte[] buffer = new byte[256 * 1024];
                for (int i = 0; i < batch.size(); i++) {
                    checkCancelled();
                    PendingBatchFile item = batch.get(i);
                    Uri destination = DocumentsContract.createDocument(
                            getContentResolver(), parent, item.mime, item.fileName);
                    if (destination == null) {
                        throw new IOException("无法创建：" + item.fileName);
                    }
                    createdDocuments.add(destination);
                    OutputStream rawOutput = getContentResolver().openOutputStream(destination, "w");
                    if (rawOutput == null) throw new IOException("无法写入：" + item.fileName);
                    try (InputStream in = new BufferedInputStream(
                                 new FileInputStream(item.file), 256 * 1024);
                         OutputStream out = new BufferedOutputStream(
                                 rawOutput, 256 * 1024)) {
                        int read;
                        while ((read = in.read(buffer)) != -1) {
                            checkCancelled();
                            out.write(buffer, 0, read);
                            copiedAll += read;
                            int progress = (int) Math.min(1000,
                                    copiedAll * 1000L / Math.max(1, totalBytes));
                            updateProgress(progress, "正在保存 " + (i + 1) + " / "
                                    + batch.size() + "：" + item.fileName);
                        }
                        out.flush();
                    }
                    item.file.delete();
                }
                checkCancelled();
                runOnUiThread(() -> {
                    cleanupPending();
                    setBusy(false);
                    statusText.setText("已分别保存 " + batch.size() + " 个文件。");
                    toast("批量保存完成");
                });
            } catch (Throwable error) {
                boolean cancelled = cancelRequested || Thread.currentThread().isInterrupted()
                        || error instanceof CancelledException;
                for (Uri uri : createdDocuments) {
                    try { DocumentsContract.deleteDocument(getContentResolver(), uri); }
                    catch (Exception ignored) { }
                }
                runOnUiThread(() -> {
                    cleanupPending();
                    setBusy(false);
                    if (cancelled) statusText.setText("已取消保存，未完成文件已清理。");
                    else statusText.setText("批量保存失败：" + safeMessage(error));
                });
            } finally {
                taskRunning = false;
                currentTask = null;
            }
        });
    }

    private void savePendingFile(Uri destination) {
        final File source = pendingOutput;
        final String savedName = pendingFileName;
        if (source == null || !source.exists()) {
            setBusy(false);
            statusText.setText("临时文件不存在，无法保存。");
            return;
        }
        cancelRequested = false;
        updateProgress(0, "正在保存文件……");
        currentTask = executor.submit(() -> {
            taskRunning = true;
            OutputStream rawOutput = null;
            try {
                rawOutput = getContentResolver().openOutputStream(destination, "w");
                if (rawOutput == null) throw new IOException("无法打开保存位置");
                try (InputStream in = new BufferedInputStream(
                             new FileInputStream(source), 256 * 1024);
                     OutputStream out = new BufferedOutputStream(
                             rawOutput, 256 * 1024)) {
                byte[] buffer = new byte[256 * 1024];
                long total = Math.max(1, source.length());
                long copied = 0;
                int read;
                while ((read = in.read(buffer)) != -1) {
                    checkCancelled();
                    out.write(buffer, 0, read);
                    copied += read;
                    int progress = (int) Math.min(1000, copied * 1000 / total);
                    updateProgress(progress, "正在保存：" + (progress / 10) + "%");
                }
                checkCancelled();
                out.flush();
                source.delete();
                runOnUiThread(() -> {
                    cleanupPending();
                    setBusy(false);
                    statusText.setText("保存成功：" + savedName);
                    toast("已保存");
                });
                }
            } catch (Throwable error) {
                boolean cancelled = cancelRequested || Thread.currentThread().isInterrupted()
                        || error instanceof CancelledException;
                if (cancelled) {
                    try { DocumentsContract.deleteDocument(getContentResolver(), destination); }
                    catch (Exception ignored) { }
                }
                runOnUiThread(() -> {
                    cleanupPending();
                    setBusy(false);
                    if (cancelled) statusText.setText("已取消保存，临时文件已清理。");
                    else statusText.setText("保存失败：" + safeMessage(error));
                });
            } finally {
                taskRunning = false;
                currentTask = null;
            }
        });
    }

    private void setBusy(boolean value) {
        busy = value;

        addButton.setEnabled(!value);
        clearButton.setEnabled(!value && !selectedItems.isEmpty());
        formatSpinner.setEnabled(!value && !visibleOutputFormats.isEmpty());
        resolutionSpinner.setEnabled(!value);
        qualitySeek.setEnabled(!value);
        fpsSpinner.setEnabled(!value);
        frameLimitSpinner.setEnabled(!value);
        bitrateSpinner.setEnabled(!value);
        loopSpinner.setEnabled(!value);
        videoLoopSpinner.setEnabled(!value);
        reverseLoopSpinner.setEnabled(!value);
        gifReplaySpinner.setEnabled(!value);
        videoGifOutputSpinner.setEnabled(!value);
        customWidthEdit.setEnabled(!value);
        customHeightEdit.setEnabled(!value);
        customFpsEdit.setEnabled(!value);
        customFrameLimitEdit.setEnabled(!value);
        customBitrateEdit.setEnabled(!value);
        customLoopEdit.setEnabled(!value);
        customVideoLoopEdit.setEnabled(!value);
        customReverseLoopEdit.setEnabled(!value);
        selectedAdapter.setLocked(value);
        if (editButton != null) {
            editButton.setEnabled(false);
            applyEditButtonStyle(editButton, false);
        }
        convertButton.setEnabled(false);
        applyButtonStyle(convertButton, false, true);
        cancelButton.setVisibility(value ? View.VISIBLE : View.GONE);
        cancelButton.setEnabled(value);
        applyButtonStyle(cancelButton, value, false);
        progressBar.setVisibility(value ? View.VISIBLE : View.GONE);
        progressText.setVisibility(value ? View.VISIBLE : View.GONE);
        if (value) {
            lastProgressPostNanos = 0L;
            lastProgressPostValue = -1;
            getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        } else {
            getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
            cancelRequested = false;
            runningSettings = null;
            updateControlStates();
            updateSelectionUi();
        }
    }


    private AnimationEdits freshAnimationEdits() {
        SharedPreferences prefs = getSharedPreferences(EDITOR_PREFS, MODE_PRIVATE);
        int brightness = clamp(prefs.getInt(
                PREF_EDITOR_BRIGHTNESS, DEFAULT_EDITOR_BRIGHTNESS), -50, 50);
        int contrast = clamp(prefs.getInt(
                PREF_EDITOR_CONTRAST, DEFAULT_EDITOR_CONTRAST), 50, 150);
        int saturation = clamp(prefs.getInt(
                PREF_EDITOR_SATURATION, DEFAULT_EDITOR_SATURATION), 0, 200);
        return new AnimationEdits(
                0.0, 0.0, 1.0, AnimationEdits.CROP_NONE, 0,
                false, false, brightness, contrast, saturation,
                Collections.emptyList(), Collections.emptyList());
    }

    private void saveEditorColorDefaults(AnimationEdits edits) {
        if (edits == null) return;
        getSharedPreferences(EDITOR_PREFS, MODE_PRIVATE).edit()
                .putInt(PREF_EDITOR_BRIGHTNESS, edits.brightness)
                .putInt(PREF_EDITOR_CONTRAST, edits.contrast)
                .putInt(PREF_EDITOR_SATURATION, edits.saturation)
                .apply();
    }

    private void resetEditorColorDefaults() {
        getSharedPreferences(EDITOR_PREFS, MODE_PRIVATE).edit()
                .putInt(PREF_EDITOR_BRIGHTNESS, DEFAULT_EDITOR_BRIGHTNESS)
                .putInt(PREF_EDITOR_CONTRAST, DEFAULT_EDITOR_CONTRAST)
                .putInt(PREF_EDITOR_SATURATION, DEFAULT_EDITOR_SATURATION)
                .apply();
    }

    private void confirmClearSelection() {
        if (selectedItems.isEmpty() || busy) return;
        new AlertDialog.Builder(this)
                .setTitle("清空选择")
                .setMessage("是否清空所有已选择的图片和视频？")
                .setNegativeButton("取消", null)
                .setPositiveButton("清空", (dialog, which) -> {
                    selectedItems.clear();
                    animationEdits = freshAnimationEdits();
                    selectedAdapter.notifyDataSetChanged();
                    updateSelectionUi();
                })
                .show();
    }

    private void updateSelectionUi() {
        if (selectionSummary == null) return;
        int images = 0;
        int videos = 0;
        int pdfs = 0;
        int texts = 0;
        int audios = 0;
        for (SelectedItem item : selectedItems) {
            if (item.isVideo()) videos++;
            else if (item.sourceFormat == SourceFormat.AUDIO) audios++;
            else if (item.sourceFormat == SourceFormat.PDF) pdfs++;
            else if (isTextSourceFormat(item.sourceFormat)) texts++;
            else images++;
        }
        if (selectedItems.isEmpty()) {
            selectionSummary.setText("尚未选择文件");
            selectedRecycler.setVisibility(View.GONE);
        } else {
            String summary = "已选择 " + selectedItems.size() + " 个文件";
            if (images > 0) summary += " · 图片 " + images;
            if (videos > 0) summary += " · 视频 " + videos;
            if (pdfs > 0) summary += " · PDF " + pdfs;
            if (texts > 0) summary += " · 文本 " + texts;
            if (audios > 0) summary += " · 音频 " + audios;
            selectionSummary.setText(summary);
            selectedRecycler.setVisibility(View.VISIBLE);
        }
        clearButton.setEnabled(!busy && !selectedItems.isEmpty());
        applyButtonStyle(clearButton, clearButton.isEnabled(), false);
        refreshOutputFormatOptions();
        updateControlStates();
    }

    private void updateActionState() {
        if (convertButton == null || busy) return;
        ActionState state = evaluateActionState();
        convertButton.setEnabled(state.enabled);
        convertButton.setText(state.enabled ? state.label : "当前无需转换");
        applyButtonStyle(convertButton, state.enabled, true);
        statusText.setText(state.enabled ? "" : state.reason);
        statusText.setVisibility(state.enabled ? View.GONE : View.VISIBLE);
    }

    private static String textOutputNames(int format) {
        return format == 35 ? "JSONL" : format == 36 ? "FB2 电子书" : TEXT_OUTPUT_NAMES[format-TEXT_FORMAT_FIRST];
    }
    private static String textOutputHints(int format) {
        return format == 35 ? "JSON 数组按元素分行；表格与结构化文本先转 JSON 再分行。"
                : format == 36 ? "提取正文生成 FB2；不保留图片、复杂版式和公式。" : TEXT_OUTPUT_HINTS[format-TEXT_FORMAT_FIRST];
    }
    private static String textOutputRequirements(int format) {
        return format == 35 ? "请选择 JSON / JSONL / CSV / TSV / YAML / XML / Markdown 表格或字幕。"
                : format == 36 ? "请选择文本、PDF 或受支持的文档。" : TEXT_OUTPUT_REQUIREMENTS[format-TEXT_FORMAT_FIRST];
    }

    /** Compatibility matrix: which source formats each text output format accepts. */
    private static boolean textConversionSupported(int format, SourceFormat source) {
        if(source == SourceFormat.RTF || source == SourceFormat.FB2) return format == 13 || format == 14 || format == 19 || format == 23 || format == 24 || format == 25 || format == 26 || format == 28 || format == 36;
        if(source == SourceFormat.JSONL) return format == 16 || format == 35 || textConversionSupported(format,SourceFormat.JSON);
        if(format == 35) return source == SourceFormat.JSON || textConversionSupported(16,source);
        if(format == 36) return isTextSourceFormat(source) || source == SourceFormat.PDF;
        boolean document = source == SourceFormat.PDF || source == SourceFormat.DOCX
                || source == SourceFormat.EPUB || source == SourceFormat.ODT;
        if (document) return format == 13 || format == 14 || format == 19
                || (format >= 23 && format <= 28 && format != 27 && !(format == 23 && source == SourceFormat.PDF));
        if (format == 24 || format == 25 || format == 26 || format == 28) return isTextSourceFormat(source);
        if ((format == 14 || format == 19) && source == SourceFormat.TXT) return true;
        if (format == 19 && source == SourceFormat.HTML) return true;
        switch (format) {
            case 13: // TXT: anything except TXT / YAML themselves
                return source != SourceFormat.TXT && source != SourceFormat.YAML;
            case 14: // HTML: Markdown, CSV, TSV, JSON
                return source == SourceFormat.MARKDOWN || source == SourceFormat.CSV
                        || source == SourceFormat.TSV || source == SourceFormat.JSON;
            case 15: // CSV: JSON, Markdown table, TSV, YAML list
                return source == SourceFormat.JSON || source == SourceFormat.MARKDOWN
                        || source == SourceFormat.TSV || source == SourceFormat.YAML;
            case 16: // JSON: CSV, Markdown table, TSV, YAML, XML, subtitles
                return source == SourceFormat.CSV || source == SourceFormat.MARKDOWN
                        || source == SourceFormat.TSV || source == SourceFormat.YAML
                        || source == SourceFormat.XML || source == SourceFormat.SRT
                        || source == SourceFormat.VTT;
            case 17: // YAML: JSON, CSV, TSV, Markdown table
                return source == SourceFormat.JSON || source == SourceFormat.CSV
                        || source == SourceFormat.TSV || source == SourceFormat.MARKDOWN;
            case 18: // XML: JSON, YAML, CSV, TSV, Markdown table
                return source == SourceFormat.JSON || source == SourceFormat.YAML
                        || source == SourceFormat.CSV || source == SourceFormat.TSV
                        || source == SourceFormat.MARKDOWN;
            case 19: // Markdown: CSV, TSV, JSON, YAML
                return source == SourceFormat.CSV || source == SourceFormat.TSV
                        || source == SourceFormat.JSON || source == SourceFormat.YAML;
            case 20: // TSV: CSV, Markdown table, JSON, YAML
                return source == SourceFormat.CSV || source == SourceFormat.MARKDOWN
                        || source == SourceFormat.JSON || source == SourceFormat.YAML;
            case 21: // VTT: SRT only
                return source == SourceFormat.SRT;
            case 22: // SRT: VTT only
                return source == SourceFormat.VTT;
            case 23: // text-to-PDF: every text source
                return true;
            default:
                return false;
        }
    }

    private ActionState evaluateActionState() {
        if (selectedItems.isEmpty()) {
            return ActionState.disabled("请先添加图片、GIF、PDF、视频或文本文件。");
        }
        int format = selectedOutputFormat();
        if (format < 0) {
            return ActionState.disabled("当前文件组合没有可直接转换的格式，请移除不兼容的文件。");
        }
        int videoCount = 0;
        int pdfCount = 0;
        int textCount = 0;
        for (SelectedItem item : selectedItems) {
            if (item.isVideo()) videoCount++;
            else if (item.sourceFormat == SourceFormat.PDF) pdfCount++;
            else if (isTextSourceFormat(item.sourceFormat)) textCount++;
        }

        if (isTextOutputFormat(format)) {
            if (textCount + pdfCount != selectedItems.size()) {
                return ActionState.disabled(
                        "文本转换接受文本、字幕、结构化数据、PDF 及支持的正文文档；请移除图片、音频或视频。");
            }
            boolean compatible = true;
            for (SelectedItem item : selectedItems) {
                if (!textConversionSupported(format, item.sourceFormat)) {
                    compatible = false;
                    break;
                }
            }
            if (!compatible) {
                return ActionState.disabled(textOutputRequirements(format));
            }
            String label = selectedItems.size() == 1
                    ? "转换为 " + textOutputNames(format)
                    : "批量转换文本（" + selectedItems.size() + " 个）";
            String hint = selectedItems.size() == 1
                    ? textOutputHints(format)
                    : "每个文本文件单独转换，完成后统一选择保存方式。";
            return ActionState.enabled(label, hint);
        }

        if (textCount > 0) {
            return ActionState.disabled(
                    "列表里包含文本或正文文档；请在输出格式里选择文本类转换，或移除这些文件。");
        }

        if (format == 9 || format == 10 || format == 27) {
            if (selectedItems.size() != 1 || (!selectedItems.get(0).isVideo() && selectedItems.get(0).sourceFormat != SourceFormat.AUDIO)) {
                return ActionState.disabled("音频转换需要且只需要一个音频或视频文件。");
            }
            if (format == 27) return ActionState.enabled("转换为 WAV", "48 kHz / 16 bit / 双声道 PCM；文件较大，不能恢复有损来源的细节。");
            if (format == 9) {
                return ActionState.enabled("转换为 MP3",
                        "将视频音轨转换为兼容性好的 192 kbps MP3。");
            }
            return ActionState.enabled("提取 M4A",
                    "AAC 音轨直接复制；其他支持的音轨自动转成 AAC-LC 48 kHz / 192 kbps。");
        }

        for (SelectedItem item : selectedItems) if (item.sourceFormat == SourceFormat.AUDIO)
            return ActionState.disabled("音频输入请选择 MP3、M4A 或 WAV 输出。");
        if (format == 11) {
            if (videoCount > 0) {
                return ActionState.disabled("PDF 输出不能包含视频，请移除视频文件。");
            }
            if (pdfCount > 0) {
                if (pdfCount != selectedItems.size() || pdfCount < 2) return ActionState.disabled("合并 PDF 请选择至少两个 PDF；图片与 PDF 请分开处理。");
                return ActionState.enabled("合并 " + pdfCount + " 个 PDF", "按列表顺序合并，保留原页面内容；签名不会延续。");
            }
            String label = selectedItems.size() == 1
                    ? "转换为 PDF" : "合成 PDF（" + selectedItems.size() + " 张）";
            return ActionState.enabled(label,
                    "每张图片占一页，按列表顺序排列；页面内使用 JPEG 压缩，动图取第一帧。");
        }

        if (format == 12) {
            if (videoCount > 0) {
                return ActionState.disabled("ICO 图标输出只接受静态图片，请移除视频。");
            }
            if (pdfCount > 0) {
                return ActionState.disabled("PDF 无法直接转 ICO，请先把 PDF 导出为图片。");
            }
            if (selectedItems.size() == 1) {
                return ActionState.enabled("生成 ICO 图标",
                        "会按图片尺寸生成 16–256 像素多个尺寸，透明背景保留，适合做 Windows/网站图标。");
            }
            return ActionState.enabled("批量生成 ICO（" + selectedItems.size() + " 张）",
                    "每张图片生成一个多尺寸 ICO 文件，最后统一选择保存方式。");
        }

        if (format >= 4 && format <= 6) {
            if (!hasOnlyVideosSelected() && (selectedItems.size() != 1 || selectedItems.get(0).sourceFormat != SourceFormat.GIF)) {
                return ActionState.disabled("MP4 输出支持一个 GIF 或一个/多个视频；不同种类请分开转换。");
            }
            if (format == 4 && !h264Supported) return ActionState.disabled("本机没有可用的 H.264 编码器。");
            if (format == 5 && !h265Supported) return ActionState.disabled("本机没有可用的 H.265 编码器。");
            if (format == 6 && !av1Supported) return ActionState.disabled("本机没有可用的 AV1 编码器，或系统版本低于 Android 14。");
            return ActionState.enabled("导出 " + videoCodecSpec(format).shortLabel + " MP4",
                    "保留剪辑效果与原声，可添加背景音乐。GIF 本身无声；声音设置中可配乐。");
        }

        if (format == 3) {
            boolean timedGif = videoCount > 0 || (selectedItems.size()==1
                    && selectedItems.get(0).sourceFormat==SourceFormat.GIF);
            if (timedGif) {
                int passes=GifPlaybackPlan.passCount(selectedVideoLoops(),selectedReverseLoop());
                if(selectedReverseLoop()>passes)return ActionState.disabled("倒放轮次不能大于内容重复次数。");
                if(selectedFrameLimit()<passes)return ActionState.disabled("帧数上限不足以容纳所有循环，请增加上限或减少重复次数。");
            }
            if (pdfCount > 0) {
                return ActionState.disabled("PDF 无法直接转 GIF，请先把 PDF 导出为图片。");
            }
            if (videoCount > 0) {
                if (videoCount != selectedItems.size()) {
                    return ActionState.disabled("视频转 GIF 暂不与静态图片混选；请只保留视频，或只保留图片。");
                }
                int videoLoops = selectedVideoLoops();
                int reverseLoop = selectedReverseLoop();
                if (reverseLoop > videoLoops) {
                    return ActionState.disabled("“第几次循环倒放”不能大于视频循环次数。");
                }
                boolean separateVideoGifs = selectedItems.size() > 1
                        && videoGifOutputSpinner != null
                        && videoGifOutputSpinner.getSelectedItemPosition() == 1;
                String label = selectedItems.size() == 1
                        ? "视频转 GIF"
                        : separateVideoGifs
                                ? "批量生成 GIF（" + selectedItems.size() + " 个）"
                                : "合成视频 GIF（" + selectedItems.size() + " 段）";
                boolean hasManualReverse = false;
                for (SelectedItem item : selectedItems) {
                    if (item.reversed) { hasManualReverse = true; break; }
                }
                String reverseHint = (hasManualReverse || reverseLoop != 0)
                        ? " 倒放会先建立帧缓存，因此速度稍慢。"
                        : "";
                String modeHint = separateVideoGifs
                        ? "每个视频生成 1 个 GIF，最后统一选择保存文件夹。"
                        : "多个视频按列表顺序合成 1 个 GIF。";
                return ActionState.enabled(label,
                        modeHint + " 视频声音不会写入 GIF。" + reverseHint);
            }
            if (selectedItems.size() == 1
                    && selectedItems.get(0).sourceFormat == SourceFormat.GIF) {
                return ActionState.enabled("重新编码 GIF", "支持重复、指定轮次倒放、全部倒放与往返播放；保留截取、变速、裁切等剪辑设置。");
            }
            if (selectedItems.size() == 1) {
                return ActionState.disabled("单张普通静态图片生成的 GIF 只有一帧，没有实际动画效果；请再添加图片，或改选 JPEG、PNG、WebP 等格式。");
            }
            return ActionState.enabled("生成 GIF（" + selectedItems.size() + " 张）",
                    "将按列表顺序生成动画。");
        }

        if (pdfCount > 0) {
            if (pdfCount != selectedItems.size()) {
                return ActionState.disabled("PDF 转图片只接受单个 PDF 文件，请移除其他文件。");
            }
            return ActionState.enabled("PDF 转 " + staticFormatName(format) + "（全部页）",
                    "逐页渲染并输出 " + staticFormatName(format)
                            + "；多页时会分别保存或打包，可在设置里调整分辨率。");
        }

        if (videoCount > 0) {
            return ActionState.disabled("静态图片格式不能接收视频，请移除视频或改选 GIF 输出。");
        }

        int resolutionPosition = resolutionSpinner == null
                ? 0 : resolutionSpinner.getSelectedItemPosition();
        boolean keepOriginal = resolutionPosition <= 1;
        boolean qualityWasTouched = qualityTouched && resolutionPosition != 0;
        boolean allNoOp = true;
        for (SelectedItem item : selectedItems) {
            if (!isExactNoOp(item, format, keepOriginal, qualityWasTouched)) {
                allNoOp = false;
                break;
            }
        }
        if (allNoOp) {
            String formatName = staticFormatName(format);
            return ActionState.disabled("所选图片已经是 " + formatName
                    + "，并且没有调整会改变文件的参数，因此无需重复转换。");
        }

        if (selectedItems.size() == 1) {
            return ActionState.enabled("转换为 " + staticFormatName(format),
                    "参数有效，可以开始转换。");
        }
        String batchReason = selectedItems.size() > ZIP_SUGGEST_THRESHOLD
                ? "开始后会询问是否打包 ZIP；也可以分别保存到一个文件夹。"
                : "转换完成后选择一个文件夹，所有图片会分别保存。";
        return ActionState.enabled("批量转换为 " + staticFormatName(format)
                        + "（" + selectedItems.size() + " 张）",
                batchReason + " 同格式且参数未改变的文件会原样复制，其余文件会转换。");
    }

    private boolean isExactNoOp(
            SelectedItem item, int outputFormat,
            boolean keepOriginalResolution, boolean qualityWasTouched) {
        if (!keepOriginalResolution || item.isVideo()) return false;
        if (outputFormat == 0) {
            return item.sourceFormat == SourceFormat.JPEG && !qualityWasTouched;
        }
        if (outputFormat == 1) return item.sourceFormat == SourceFormat.PNG;
        if (outputFormat == 2) return item.sourceFormat == SourceFormat.BMP;
        return false;
    }

    private String staticFormatName(int format) {
        if (format == 0) return "JPEG";
        if (format == 1) return "PNG";
        if (format == 2) return "BMP";
        if (format == 7) return "WebP 有损";
        if (format == 8) return "WebP 无损";
        if(format>=29&&format<=34)return new String[]{"TIFF","TGA","PPM","PGM","PBM","PAM"}[format-29];
        return "图片";
    }

    private void cancelActiveTask() {
        if (!busy || cancelRequested) return;
        cancelRequested = true;
        cancelButton.setEnabled(false);
        applyButtonStyle(cancelButton, false, false);
        statusText.setText("已请求取消，正在安全停止当前步骤……");
        progressText.setText("正在取消；通常会在当前一帧处理完成后停止");
        Future<?> task = currentTask;
        boolean futureCancelled = task != null && task.cancel(true);
        if (futureCancelled && !taskRunning) {
            cancelButton.post(() -> {
                if (currentTask == task && !taskRunning) {
                    currentTask = null;
                    finishCancelledUi();
                }
            });
            return;
        }
        if (task == null && (pendingOutput != null
                || (pendingBatchFiles != null && !pendingBatchFiles.isEmpty()))) {
            cleanupPending();
            setBusy(false);
            statusText.setText("已取消转换。");
        }
    }

    private void finishCancelledUi() {
        cleanupPending();
        deleteActiveWorkFile();
        setBusy(false);
        // Keep stale completion callbacks from reopening the save picker. A new task explicitly
        // clears this flag before it starts.
        cancelRequested = true;
        statusText.setText("已取消转换。");
    }

    private void deleteActiveWorkFile() {
        File file = activeWorkFile;
        activeWorkFile = null;
        if (file != null && file.exists()) file.delete();
    }

    private void copyUriToStream(Uri uri, OutputStream out) throws Exception {
        InputStream raw = getContentResolver().openInputStream(uri);
        if (raw == null) throw new IOException("无法读取源文件");
        try (InputStream in = new BufferedInputStream(raw)) {
            byte[] buffer = new byte[256 * 1024];
            int read;
            while ((read = in.read(buffer)) != -1) {
                checkCancelled();
                out.write(buffer, 0, read);
            }
        }
    }

    private String uniqueEntryName(String requested, Set<String> usedNames) {
        String candidate = requested;
        int dot = requested.lastIndexOf('.');
        String base = dot > 0 ? requested.substring(0, dot) : requested;
        String ext = dot > 0 ? requested.substring(dot) : "";
        int number = 2;
        while (!usedNames.add(candidate.toLowerCase(Locale.ROOT))) {
            candidate = base + "_" + number++ + ext;
        }
        return candidate;
    }

    private long queryFileSize(Uri uri) {
        try (Cursor cursor = getContentResolver().query(
                uri, new String[]{OpenableColumns.SIZE}, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int index = cursor.getColumnIndex(OpenableColumns.SIZE);
                if (index >= 0 && !cursor.isNull(index)) return cursor.getLong(index);
            }
        } catch (Exception ignored) { }
        return -1;
    }

    private SourceFormat detectSourceFormat(Uri uri, String name, String mime) {
        String lowerMime = mime == null ? "" : mime.toLowerCase(Locale.ROOT);
        String lowerName = name == null ? "" : name.toLowerCase(Locale.ROOT);
        if (lowerName.endsWith(".rtf") || lowerMime.equals("application/rtf") || lowerMime.equals("text/rtf")) return SourceFormat.RTF;
        if (lowerName.endsWith(".fb2") || lowerMime.equals("application/x-fictionbook+xml")) return SourceFormat.FB2;
        if (lowerName.endsWith(".jsonl") || lowerName.endsWith(".ndjson") || lowerMime.equals("application/x-ndjson")) return SourceFormat.JSONL;
        if (lowerName.matches(".*\\.(tif|tiff|tga|ppm|pgm|pbm|pnm|pam|svg|svgz|avif)$")) return SourceFormat.OTHER_IMAGE;
        if (lowerMime.equals("application/pdf") || lowerName.endsWith(".pdf")) {
            return SourceFormat.PDF;
        }
        if (lowerName.endsWith(".docx") || lowerMime.contains("wordprocessingml")) return SourceFormat.DOCX;
        if (lowerName.endsWith(".epub") || lowerMime.equals("application/epub+zip")) return SourceFormat.EPUB;
        if (lowerName.endsWith(".odt") || lowerMime.equals("application/vnd.oasis.opendocument.text")) return SourceFormat.ODT;
        if (lowerMime.startsWith("audio/") || lowerName.matches(".*\\.(mp3|m4a|aac|wav|flac|ogg|opus|amr|aiff|aif)$")) return SourceFormat.AUDIO;
        if (lowerMime.startsWith("video/") || isVideoByName(lowerName)) return SourceFormat.VIDEO;
        if (lowerMime.equals("image/jpeg") || lowerName.endsWith(".jpg") || lowerName.endsWith(".jpeg")) return SourceFormat.JPEG;
        if (lowerMime.equals("image/png") || lowerName.endsWith(".png")) return SourceFormat.PNG;
        if (lowerMime.equals("image/bmp") || lowerName.endsWith(".bmp")) return SourceFormat.BMP;
        if (lowerMime.equals("image/gif") || lowerName.endsWith(".gif")) return SourceFormat.GIF;
        if (lowerMime.equals("image/webp") || lowerName.endsWith(".webp")) return SourceFormat.WEBP;
        if (lowerMime.contains("heic") || lowerMime.contains("heif")
                || lowerName.endsWith(".heic") || lowerName.endsWith(".heif")) return SourceFormat.HEIC;
        if (lowerName.endsWith(".md") || lowerName.endsWith(".markdown") || lowerName.endsWith(".mdown")
                || lowerMime.equals("text/markdown")) return SourceFormat.MARKDOWN;
        if (lowerName.endsWith(".html") || lowerName.endsWith(".htm")
                || lowerMime.equals("text/html")) return SourceFormat.HTML;
        if (lowerName.endsWith(".csv") || lowerMime.equals("text/csv")
                || lowerMime.equals("application/csv")) return SourceFormat.CSV;
        if (lowerName.endsWith(".json") || lowerMime.equals("application/json")) return SourceFormat.JSON;
        if (lowerName.endsWith(".tsv") || lowerMime.equals("text/tab-separated-values")) return SourceFormat.TSV;
        if (lowerName.endsWith(".yaml") || lowerName.endsWith(".yml")
                || lowerMime.equals("application/yaml") || lowerMime.equals("application/x-yaml")
                || lowerMime.equals("text/yaml")) return SourceFormat.YAML;
        if (lowerName.endsWith(".xml") || lowerMime.equals("application/xml")
                || lowerMime.equals("text/xml")
                || lowerMime.equals("application/rss+xml")) return SourceFormat.XML;
        if (lowerName.endsWith(".srt") || lowerMime.equals("application/x-subrip")
                || lowerMime.equals("application/subrip")) return SourceFormat.SRT;
        if (lowerName.endsWith(".vtt") || lowerMime.equals("text/vtt")) return SourceFormat.VTT;
        if (lowerName.endsWith(".txt") || lowerMime.equals("text/plain")) return SourceFormat.TXT;
        if (lowerMime.startsWith("image/")) return SourceFormat.OTHER_IMAGE;
        return SourceFormat.UNKNOWN;
    }

    private boolean isVideoByName(String lowerName) {
        return lowerName.endsWith(".mp4") || lowerName.endsWith(".m4v")
                || lowerName.endsWith(".mov") || lowerName.endsWith(".mkv")
                || lowerName.endsWith(".webm") || lowerName.endsWith(".avi")
                || lowerName.endsWith(".3gp") || lowerName.endsWith(".mpeg")
                || lowerName.endsWith(".mpg");
    }

    private Bitmap loadThumbnail(SelectedItem item) {
        String key = item.uri.toString();
        Bitmap cached = thumbnailCache.get(key);
        if (cached != null) return cached;
        Bitmap bitmap = null;
        try {
            if (item.isVideo()) {
                MediaMetadataRetriever retriever = new MediaMetadataRetriever();
                try {
                    retriever.setDataSource(this, item.uri);
                    bitmap = retriever.getScaledFrameAtTime(
                            0, MediaMetadataRetriever.OPTION_CLOSEST_SYNC, dp(96), dp(96));
                    // Keep the placeholder if a vendor cannot provide a scaled thumbnail.
                } finally {
                    retriever.release();
                }
            } else if (item.sourceFormat == SourceFormat.PDF) {
                bitmap = loadPdfThumbnail(item.uri);
            } else if (isTextSourceFormat(item.sourceFormat) || item.sourceFormat == SourceFormat.AUDIO) {
                bitmap = textThumbnail(item.sourceFormat);
            } else if(!ExtraImageFormats.kind(this,item.uri).isEmpty()) {
                bitmap=decodeBitmap(item.uri,dp(96),dp(96),65536);
            } else {
                ImageDecoder.Source source = ImageDecoder.createSource(getContentResolver(), item.uri);
                bitmap = ImageDecoder.decodeBitmap(source, (decoder, info, src) -> {
                    decoder.setAllocator(ImageDecoder.ALLOCATOR_SOFTWARE);
                    int[] size = fitSize(info.getSize().getWidth(), info.getSize().getHeight(),
                            dp(96), dp(96), true);
                    decoder.setTargetSize(Math.max(1, size[0]), Math.max(1, size[1]));
                });
            }
            if (bitmap != null) {
                Bitmap square = fitOnCanvas(bitmap, dp(72), dp(72), 0xFFF0F1F5);
                if (square != bitmap) bitmap.recycle();
                bitmap = square;
                thumbnailCache.put(key, bitmap);
            }
        } catch (Exception ignored) { }
        return bitmap;
    }

    private Bitmap loadPdfThumbnail(Uri uri) {
        ParcelFileDescriptor handle = null;
        try {
            handle = getContentResolver().openFileDescriptor(uri, "r");
            if (handle == null) return null;
            try (PdfRenderer renderer = new PdfRenderer(handle)) {
                if (renderer.getPageCount() <= 0) return null;
                try (PdfRenderer.Page page = renderer.openPage(0)) {
                    int side = dp(96);
                    int[] size = fitSize(
                            page.getWidth(), page.getHeight(), side, side, true);
                    Bitmap bitmap = Bitmap.createBitmap(
                            Math.max(1, size[0]), Math.max(1, size[1]),
                            Bitmap.Config.ARGB_8888);
                    bitmap.eraseColor(0xFFFFFFFF);
                    page.render(bitmap, null, null,
                            PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY);
                    return bitmap;
                }
            }
        } catch (Throwable ignored) {
            return null;
        } finally {
            if (handle != null) {
                try { handle.close(); } catch (Exception ignored) { }
            }
        }
    }

    private void applyButtonStyle(Button button, boolean enabled, boolean primary) {
        button.setTextColor(0xFFFFFFFF);
        int color;
        if (!enabled) color = DISABLED;
        else color = primary ? PRIMARY : 0xFF777A88;
        button.setBackground(roundRect(color, 14));
        button.setAlpha(1f);
    }


    private void applyEditButtonStyle(Button button, boolean enabled) {
        GradientDrawable background = roundRect(enabled ? 0xFFF0EFFF : 0xFFF0F1F5, 14);
        background.setStroke(dp(1), enabled ? PRIMARY : 0xFFD3D5DD);
        button.setBackground(background);
        button.setTextColor(enabled ? PRIMARY : 0xFF8A8C96);
        button.setAlpha(1f);
    }

    private void addTwoButtons(LinearLayout row, View first, View second) {
        LinearLayout.LayoutParams left = new LinearLayout.LayoutParams(0, dp(52), 2f);
        left.setMarginEnd(dp(5));
        LinearLayout.LayoutParams right = new LinearLayout.LayoutParams(0, dp(52), 1f);
        right.setMarginStart(dp(5));
        row.addView(first, left);
        row.addView(second, right);
    }

    private static String safeMessage(Throwable error) {
        if (error instanceof OutOfMemoryError) {
            return "设备可用内存不足，请使用智能推荐或降低分辨率和帧数";
        }
        String message = error.getMessage();
        if (message != null && (message.contains("ENOSPC")
                || message.toLowerCase(Locale.ROOT).contains("no space"))) {
            return "存储空间不足，请清理空间后重试";
        }
        return message == null || message.trim().isEmpty()
                ? error.getClass().getSimpleName() : message;
    }

    private static int thumbnailCacheKilobytes() {
        long suggested = Runtime.getRuntime().maxMemory() / (24L * 1024L);
        return (int) Math.max(4 * 1024L, Math.min(16 * 1024L, suggested));
    }

    private void ensureCacheCapacity() throws IOException {
        ensureCacheCapacity(0L);
    }

    private void ensureCacheCapacity(long expectedBytes) throws IOException {
        long usable = getCacheDir().getUsableSpace();
        long reserve = 32L * 1024 * 1024;
        long required = saturatingAdd(reserve, Math.max(0L, expectedBytes));
        if (usable > 0 && usable < required) {
            long requiredMb = Math.max(32L,
                    (required + 1024L * 1024L - 1L) / (1024L * 1024L));
            throw new IOException("临时存储空间不足，当前任务预计至少需要 "
                    + requiredMb + " MB");
        }
    }

    private static long estimatedGifOutputBytes(int width, int height, long frames) {
        long pixels = saturatingMultiply(
                Math.max(1L, (long) width * height), Math.max(1L, frames));
        return Math.max(8L * 1024 * 1024, pixels / 2L);
    }

    private static long estimatedStaticOutputBytes(int format, int width, int height) {
        long pixels = Math.max(1L, (long) width * height);
        if (format == 2) {
            long rowBytes = (((long) width * 3L) + 3L) & ~3L;
            return saturatingAdd(54L, saturatingMultiply(rowBytes, height));
        }
        if (format == 1 || format == 8 || (format >= 29 && format <= 34)) return saturatingAdd(65536,saturatingMultiply(pixels, 4L));
        return pixels;
    }

    private synchronized void updateProgress(int progress, String message) {
        int localProgress = clamp(progress, 0, 1000);
        int mappedProgress = progressMapStart
                + (int) (localProgress * (long) progressMapSpan / 1000L);
        final int safeProgress = clamp(mappedProgress, 0, 1000);
        final String safeMessage = (progressMapPrefix == null ? "" : progressMapPrefix)
                + (message == null ? "" : message);
        long now = System.nanoTime();
        boolean force = lastProgressPostValue < 0
                || (safeProgress == 0 && lastProgressPostValue != 0)
                || (safeProgress == 1000 && lastProgressPostValue != 1000)
                || now - lastProgressPostNanos >= 100_000_000L;
        if (!force) return;
        lastProgressPostValue = safeProgress;
        lastProgressPostNanos = now;
        runOnUiThread(() -> {
            if (isDestroyed()) return;
            progressBar.setProgress(safeProgress);
            progressText.setText(safeMessage);
        });
    }

    private void checkCancelled() throws CancelledException {
        if (isCancellationRequested()) {
            throw new CancelledException();
        }
    }

    private boolean isCancellationRequested() {
        return cancelRequested || Thread.currentThread().isInterrupted();
    }

    private void cleanupPending() {
        if (pendingOutput != null && pendingOutput.exists()) pendingOutput.delete();
        pendingOutput = null;
        pendingFileName = null;
        if (pendingBatchFiles != null) deleteBatchFiles(pendingBatchFiles);
        pendingBatchFiles = null;
    }

    private void deleteBatchFiles(List<PendingBatchFile> files) {
        if (files == null) return;
        for (PendingBatchFile item : files) {
            if (item != null && item.file != null && item.file.exists()) item.file.delete();
        }
    }

    private boolean isVideo(Uri uri) {
        String type = getContentResolver().getType(uri);
        if (type != null && type.startsWith("video/")) return true;
        return isVideoByName(queryDisplayName(uri).toLowerCase(Locale.ROOT));
    }

    private String queryDisplayName(Uri uri) {
        try (Cursor cursor = getContentResolver().query(
                uri, new String[]{OpenableColumns.DISPLAY_NAME}, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (index >= 0) return cursor.getString(index);
            }
        } catch (Exception ignored) { }
        return "文件";
    }

    private void refreshCodecSupportText() {
        h264Supported = Mp4Encoder.hasSurfaceEncoder(Mp4Encoder.MIME_H264);
        h265Supported = Mp4Encoder.hasSurfaceEncoder(Mp4Encoder.MIME_H265);
        av1Supported = Build.VERSION.SDK_INT >= 34
                && Mp4Encoder.hasSurfaceEncoder(Mp4Encoder.MIME_AV1);
        codecSupportText.setText(
                "本机编码器：H.264 " + supportWord(h264Supported)
                        + "　H.265 " + supportWord(h265Supported)
                        + "　AV1 " + supportWord(av1Supported));
        refreshOutputFormatOptions();
        updateActionState();
    }

    private String supportWord(boolean supported) {
        return supported ? "支持" : "不支持";
    }

    private VideoCodecSpec videoCodecSpec(int format) {
        switch (format) {
            case 4:
                return new VideoCodecSpec(
                        Mp4Encoder.MIME_H264, "H.264/AVC", "H.264", "h264");
            case 5:
                return new VideoCodecSpec(
                        Mp4Encoder.MIME_H265, "H.265/HEVC", "H.265", "h265");
            case 6:
                return new VideoCodecSpec(
                        Mp4Encoder.MIME_AV1, "AV1", "AV1", "av1");
            default:
                throw new IllegalArgumentException("未知视频编码格式");
        }
    }

    private OutputSpec outputSpec(int format) {
        switch (format) {
            case 0: return new OutputSpec(".jpg", "image/jpeg", "JPEG");
            case 1: return new OutputSpec(".png", "image/png", "PNG");
            case 2: return new OutputSpec(".bmp", "image/bmp", "BMP");
            case 7:
            case 8: return new OutputSpec(".webp", "image/webp", format == 7 ? "WEBP_LOSSY" : "WEBP_LOSSLESS");
            case 11: return new OutputSpec(".pdf", "application/pdf", "PDF");
            case 12: return new OutputSpec(".ico", "image/x-icon", "ICO");
            case 13: return new OutputSpec(".txt", "text/plain", "TXT");
            case 14: return new OutputSpec(".html", "text/html", "HTML");
            case 15: return new OutputSpec(".csv", "text/csv", "CSV");
            case 16: return new OutputSpec(".json", "application/json", "JSON");
            case 17: return new OutputSpec(".yaml", "application/yaml", "YAML");
            case 18: return new OutputSpec(".xml", "application/xml", "XML");
            case 19: return new OutputSpec(".md", "text/markdown", "MD");
            case 20: return new OutputSpec(".tsv", "text/tab-separated-values", "TSV");
            case 21: return new OutputSpec(".vtt", "text/vtt", "VTT");
            case 22: return new OutputSpec(".srt", "application/x-subrip", "SRT");
            case 23: return new OutputSpec(".pdf", "application/pdf", "PDF");
            case 24: return new OutputSpec(".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "DOCX");
            case 25: return new OutputSpec(".epub", "application/epub+zip", "EPUB");
            case 26: return new OutputSpec(".odt", "application/vnd.oasis.opendocument.text", "ODT");
            case 27: return new OutputSpec(".wav", "audio/wav", "WAV");
            case 28: return new OutputSpec(".rtf", "application/rtf", "RTF");
            case 29: return new OutputSpec(".tiff", "image/tiff", "TIFF");
            case 30: return new OutputSpec(".tga", "image/x-tga", "TGA");
            case 31: return new OutputSpec(".ppm", "image/x-portable-pixmap", "PPM");
            case 32: return new OutputSpec(".pgm", "image/x-portable-graymap", "PGM");
            case 33: return new OutputSpec(".pbm", "image/x-portable-bitmap", "PBM");
            case 34: return new OutputSpec(".pam", "image/x-portable-arbitrarymap", "PAM");
            case 35: return new OutputSpec(".jsonl", "application/x-ndjson", "JSONL");
            case 36: return new OutputSpec(".fb2", "application/x-fictionbook+xml", "FB2");
            default: throw new IllegalArgumentException("未知格式");
        }
    }

    private void cleanupStaleConversionFiles() {
        File[] files = getCacheDir().listFiles();
        if (files == null) return;
        for (File file : files) {
            String name = file.getName();
            if (file.isFile()
                    && (name.startsWith("converted_") || name.startsWith("gif_frames_") || name.startsWith("audio_") || name.startsWith("document_") || name.startsWith("video_frames_") || name.startsWith("image_"))) {
                try { file.delete(); } catch (Exception ignored) { }
            }
        }
    }

    private File cacheFile(String extension) {
        File file = new File(getCacheDir(), "converted_" + System.nanoTime() + extension);
        activeWorkFile = file;
        return file;
    }

    private static String lockedFileSuffix(String name) {
        if (name == null) return "";
        int dot = name.lastIndexOf('.');
        if (dot <= 0 || dot >= name.length() - 1) return "";
        String suffix = name.substring(dot);
        if (suffix.length() > 16 || suffix.indexOf('/') >= 0 || suffix.indexOf('\\') >= 0) {
            return "";
        }
        return suffix;
    }

    private static String editableFileBase(String name) {
        if (name == null || name.trim().isEmpty()) return "converted";
        String suffix = lockedFileSuffix(name);
        return suffix.isEmpty() ? name : name.substring(0, name.length() - suffix.length());
    }

    private static String sanitizeRenamedBase(String value) {
        if (value == null) return "";
        return value.replace('\n', ' ').replace('\r', ' ')
                .replaceAll("[\\/:*?\"<>|]", "_").trim();
    }

    private String safeBaseName(String name) {
        if (name == null || name.trim().isEmpty()) return "converted";
        int dot = name.lastIndexOf('.');
        String base = dot > 0 ? name.substring(0, dot) : name;
        base = base.replaceAll("[\\\\/:*?\"<>|]", "_").trim();
        return base.isEmpty() ? "converted" : base;
    }

    private static int parseInt(String text, int fallback) {
        try { return Integer.parseInt(text.trim()); }
        catch (Exception e) { return fallback; }
    }

    private static long parseLong(String text, long fallback) {
        try { return Long.parseLong(text); }
        catch (Exception e) { return fallback; }
    }

    private static double parseDouble(String text, double fallback) {
        try { return Math.max(0, Double.parseDouble(text.trim())); }
        catch (Exception e) { return fallback; }
    }

    private static int makeEven(int value) {
        return value % 2 == 0 ? value : value - 1;
    }

    private static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }

    private static long saturatingAdd(long first, long second) {
        if (first >= Long.MAX_VALUE - second) return Long.MAX_VALUE;
        return first + second;
    }

    private static long saturatingMultiply(long first, long second) {
        if (first <= 0 || second <= 0) return 0;
        if (first > Long.MAX_VALUE / second) return Long.MAX_VALUE;
        return first * second;
    }

    private TextView text(String content, int size, int color, boolean bold) {
        TextView view = new TextView(this);
        view.setText(content);
        view.setTextSize(size);
        view.setTextColor(color);
        if (bold) view.setTypeface(null, 1);
        return view;
    }

    private TextView addLabel(LinearLayout parent, String label, int color) {
        TextView view = text(label, 15, color, true);
        view.setPadding(0, 0, 0, dp(5));
        parent.addView(view);
        return view;
    }

    private TextView addLabelWithTop(LinearLayout parent, String label, int color) {
        TextView view = text(label, 15, color, true);
        view.setPadding(0, dp(17), 0, dp(5));
        parent.addView(view);
        return view;
    }

    private void setViewsVisible(boolean visible, View... views) {
        int visibility = visible ? View.VISIBLE : View.GONE;
        for (View view : views) {
            if (view != null && view.getVisibility() != visibility) {
                view.setVisibility(visibility);
            }
        }
    }

    private Spinner createSpinner(String[] values) {
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
    }

    private EditText numberField(String hint, String value, boolean decimal) {
        EditText edit = new EditText(this);
        edit.setHint(hint);
        edit.setText(value);
        edit.setSingleLine(true);
        edit.setTextSize(14);
        edit.setInputType(InputType.TYPE_CLASS_NUMBER
                | (decimal ? InputType.TYPE_NUMBER_FLAG_DECIMAL : 0));
        edit.setPadding(dp(12), 0, dp(12), 0);
        edit.setBackground(roundRect(0xFFF0F1F5, 12));
        return edit;
    }

    private Button createEditorButton(String label, boolean primary) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setTextSize(13);
        button.setTypeface(null, 1);
        button.setMinHeight(0);
        button.setMinimumHeight(0);
        button.setMinWidth(0);
        button.setMinimumWidth(0);
        button.setPadding(dp(8), 0, dp(8), 0);
        applyEditorButtonStyle(button, true, primary);
        return button;
    }

    private void applyEditorButtonStyle(Button button, boolean enabled, boolean primary) {
        button.setTextColor(enabled ? 0xFFFFFFFF : 0xFFEEF0F5);
        int color = !enabled ? 0xFFB6B8C2 : (primary ? PRIMARY : 0xFF666978);
        button.setBackground(roundRect(color, 10));
        button.setAlpha(enabled ? 1f : 0.72f);
    }

    private void addCompactButtons(LinearLayout row, Button... buttons) {
        for (int i = 0; i < buttons.length; i++) {
            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                    0, dp(40), 1f);
            if (i > 0) params.setMarginStart(dp(3));
            if (i + 1 < buttons.length) params.setMarginEnd(dp(3));
            row.addView(buttons[i], params);
        }
    }

    private static String formatTimelineTime(double seconds) {
        double safe = Math.max(0.0, seconds);
        int minutes = (int) (safe / 60.0);
        double remaining = safe - minutes * 60.0;
        return String.format(Locale.CHINA, "%d:%05.2f", minutes, remaining);
    }

    private Button createButton(String label, boolean primary) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setTextSize(16);
        button.setTypeface(null, 1);
        button.setMinHeight(dp(52));
        applyButtonStyle(button, true, primary);
        return button;
    }

    private LinearLayout horizontalRow() {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(0, dp(8), 0, 0);
        return row;
    }

    private void addTwoFields(LinearLayout row, View first, View second) {
        LinearLayout.LayoutParams left = new LinearLayout.LayoutParams(0, dp(54), 1f);
        left.setMarginEnd(dp(5));
        LinearLayout.LayoutParams right = new LinearLayout.LayoutParams(0, dp(54), 1f);
        right.setMarginStart(dp(5));
        row.addView(first, left);
        row.addView(second, right);
    }

    private LinearLayout.LayoutParams fieldParams() {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(54));
        params.topMargin = dp(7);
        return params;
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private GradientDrawable roundRect(int color, int radiusDp) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(dp(radiusDp));
        return drawable;
    }

    private SeekBar.OnSeekBarChangeListener seekListener(Runnable callback) {
        return new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar s, int p, boolean f) {
                callback.run();
            }
            @Override public void onStartTrackingTouch(SeekBar s) { }
            @Override public void onStopTrackingTouch(SeekBar s) { }
        };
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private void toast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onPause() {
        if (pauseEditorPreview != null) pauseEditorPreview.run();
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        if (activeAudioDialog != null) activeAudioDialog.dismiss();
        if (activeEditorDialog != null) activeEditorDialog.dismiss();
        cancelRequested = true;
        Future<?> task = currentTask;
        if (task != null) task.cancel(true);
        executor.shutdownNow();
        thumbnailExecutor.shutdownNow();
        recommendationGeneration++;
        recommendationHandler.removeCallbacksAndMessages(null);
        recommendationExecutor.shutdownNow();
        thumbnailCache.evictAll();
        deleteActiveWorkFile();
        cleanupPending();
        super.onDestroy();
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        if (level >= ComponentCallbacks2.TRIM_MEMORY_RUNNING_LOW) {
            thumbnailCache.trimToSize(thumbnailCache.maxSize() / 4);
        }
    }

    @Override
    public void onLowMemory() {
        thumbnailCache.evictAll();
        super.onLowMemory();
    }

    private static final class VideoCodecSpec {
        final String mime;
        final String label;
        final String shortLabel;
        final String fileSuffix;

        VideoCodecSpec(String mime, String label, String shortLabel, String fileSuffix) {
            this.mime = mime;
            this.label = label;
            this.shortLabel = shortLabel;
            this.fileSuffix = fileSuffix;
        }
    }

    private final class SelectedFileAdapter extends RecyclerView.Adapter<SelectedFileAdapter.Holder> {
        private boolean locked;

        void setLocked(boolean value) {
            locked = value;
            notifyDataSetChanged();
        }

        @Override public Holder onCreateViewHolder(ViewGroup parent, int viewType) {
            LinearLayout row = new LinearLayout(MainActivity.this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(dp(8), dp(8), dp(8), dp(8));
            row.setBackground(roundRect(0xFFF0F1F5, 13));
            RecyclerView.LayoutParams params = new RecyclerView.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(88));
            params.bottomMargin = dp(7);
            row.setLayoutParams(params);

            FrameLayout thumbnailFrame = new FrameLayout(MainActivity.this);
            row.addView(thumbnailFrame, new LinearLayout.LayoutParams(dp(72), dp(72)));

            ImageView thumbnail = new ImageView(MainActivity.this);
            thumbnail.setScaleType(ImageView.ScaleType.CENTER_CROP);
            thumbnail.setBackground(new ColorDrawable(0xFFE2E3E9));
            thumbnailFrame.addView(thumbnail, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

            TextView remove = text("×", 18, 0xFFFFFFFF, true);
            remove.setGravity(Gravity.CENTER);
            remove.setContentDescription("移除这个文件");
            remove.setBackground(roundRect(0xD94A4C57, 14));
            FrameLayout.LayoutParams removeParams = new FrameLayout.LayoutParams(dp(28), dp(28));
            removeParams.gravity = Gravity.TOP | Gravity.END;
            removeParams.setMargins(0, dp(3), dp(3), 0);
            thumbnailFrame.addView(remove, removeParams);

            LinearLayout info = new LinearLayout(MainActivity.this);
            info.setOrientation(LinearLayout.VERTICAL);
            info.setGravity(Gravity.CENTER_VERTICAL);
            LinearLayout.LayoutParams infoParams = new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.MATCH_PARENT, 1f);
            infoParams.setMarginStart(dp(10));
            row.addView(info, infoParams);

            FrameLayout nameFrame = new FrameLayout(MainActivity.this);
            info.addView(nameFrame, matchWrap());

            TextView name = text("", 14, PRIMARY_TEXT, true);
            name.setSingleLine(true);
            name.setEllipsize(android.text.TextUtils.TruncateAt.MIDDLE);
            name.setClickable(true);
            nameFrame.addView(name, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            LinearLayout renameRow = new LinearLayout(MainActivity.this);
            renameRow.setOrientation(LinearLayout.HORIZONTAL);
            renameRow.setGravity(Gravity.CENTER_VERTICAL);
            renameRow.setVisibility(View.GONE);
            nameFrame.addView(renameRow, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            EditText renameEdit = new EditText(MainActivity.this);
            renameEdit.setSingleLine(true);
            renameEdit.setTextSize(14);
            renameEdit.setTextColor(PRIMARY_TEXT);
            renameEdit.setTypeface(null, 1);
            renameEdit.setPadding(0, 0, 0, 0);
            renameEdit.setBackgroundColor(Color.TRANSPARENT);
            renameEdit.setImeOptions(android.view.inputmethod.EditorInfo.IME_ACTION_DONE);
            renameEdit.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                    | android.text.InputType.TYPE_TEXT_FLAG_CAP_SENTENCES);
            renameRow.addView(renameEdit, new LinearLayout.LayoutParams(
                    0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

            TextView renameSuffix = text("", 14, PRIMARY_TEXT, false);
            renameSuffix.setSingleLine(true);
            renameRow.addView(renameSuffix, new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            TextView detail = text("", 12, SECONDARY_TEXT, false);
            detail.setPadding(0, dp(4), 0, 0);
            info.addView(detail, matchWrap());
            return new Holder(row, thumbnail, name, renameRow, renameEdit, renameSuffix, detail, remove);
        }

        @Override public void onBindViewHolder(Holder holder, int position) {
            SelectedItem item = selectedItems.get(position);
            holder.renaming = false;
            holder.renameEdit.setOnFocusChangeListener(null);
            holder.renameEdit.clearFocus();
            holder.renameRow.setVisibility(View.GONE);
            holder.name.setVisibility(View.VISIBLE);
            holder.name.setText((position + 1) + ". " + item.name);
            holder.detail.setText(sourceFormatLabel(item.sourceFormat)
                    + (item.size >= 0 ? " · " + humanSize(item.size) : "")
                    + (item.copied ? " · 副本" : "")
                    + (item.reversed ? " · 倒放" : ""));
            holder.remove.setAlpha(locked ? 0.4f : 1f);
            holder.itemView.setContentDescription(item.isVideo()
                    ? "长按拖动排序；点按打开视频操作"
                    : "长按拖动排序");
            holder.name.setOnClickListener(v -> {
                if (locked) return;
                beginInlineRename(holder);
            });
            holder.name.setOnLongClickListener(v -> {
                if (locked) return false;
                if (holder.renaming) commitInlineRename(holder);
                itemTouchHelper.startDrag(holder);
                return true;
            });
            holder.remove.setOnClickListener(v -> {
                if (locked) return;
                int p = holder.getBindingAdapterPosition();
                if (p == RecyclerView.NO_POSITION) return;
                SelectedItem removed = selectedItems.remove(p);
                animationEdits = freshAnimationEdits();
                thumbnailCache.remove(removed.uri.toString());
                notifyItemRemoved(p);
                notifyItemRangeChanged(p, selectedItems.size() - p);
                updateSelectionUi();
            });
            holder.itemView.setOnClickListener(v -> {
                if (locked) return;
                if (holder.renaming) {
                    commitInlineRename(holder);
                    return;
                }
                int p = holder.getBindingAdapterPosition();
                if (p == RecyclerView.NO_POSITION) return;
                SelectedItem current = selectedItems.get(p);
                if (current.isVideo()) {
                    showVideoItemMenu(holder.itemView, p);
                }
            });
            holder.itemView.setOnLongClickListener(v -> {
                if (locked) return false;
                if (holder.renaming) commitInlineRename(holder);
                itemTouchHelper.startDrag(holder);
                return true;
            });

            String key = item.uri.toString();
            holder.thumbnail.setTag(key);
            Bitmap cached = thumbnailCache.get(key);
            if (cached != null) {
                holder.thumbnail.setImageBitmap(cached);
            } else {
                holder.thumbnail.setImageResource(item.isVideo()
                        ? android.R.drawable.ic_media_play
                        : android.R.drawable.ic_menu_gallery);
                thumbnailExecutor.execute(() -> {
                    if (isDestroyed() || Thread.currentThread().isInterrupted()) return;
                    Bitmap loaded = loadThumbnail(item);
                    runOnUiThread(() -> {
                        if (!isDestroyed() && key.equals(holder.thumbnail.getTag()) && loaded != null) {
                            holder.thumbnail.setImageBitmap(loaded);
                        }
                    });
                });
            }
        }

        private void beginInlineRename(Holder holder) {
            if (holder == null || holder.renaming || locked) return;
            int position = holder.getBindingAdapterPosition();
            if (position == RecyclerView.NO_POSITION) return;
            SelectedItem item = selectedItems.get(position);
            String suffix = lockedFileSuffix(item.name);
            String base = editableFileBase(item.name);
            holder.renaming = true;
            holder.renameSuffix.setText(suffix);
            holder.renameEdit.setText(base);
            holder.name.setVisibility(View.GONE);
            holder.renameRow.setVisibility(View.VISIBLE);
            holder.renameEdit.setOnFocusChangeListener((view, hasFocus) -> {
                if (!hasFocus) commitInlineRename(holder);
            });
            holder.renameEdit.setOnEditorActionListener((view, actionId, event) -> {
                boolean enter = actionId == android.view.inputmethod.EditorInfo.IME_ACTION_DONE
                        || (event != null
                        && event.getKeyCode() == android.view.KeyEvent.KEYCODE_ENTER
                        && event.getAction() == android.view.KeyEvent.ACTION_UP);
                if (!enter) return false;
                commitInlineRename(holder);
                return true;
            });
            holder.renameEdit.requestFocus();
            holder.renameEdit.setSelection(0, holder.renameEdit.length());
            android.view.inputmethod.InputMethodManager keyboard =
                    (android.view.inputmethod.InputMethodManager) getSystemService(
                            android.content.Context.INPUT_METHOD_SERVICE);
            if (keyboard != null) keyboard.showSoftInput(
                    holder.renameEdit, android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);
        }

        private void commitInlineRename(Holder holder) {
            if (holder == null || !holder.renaming) return;
            int position = holder.getBindingAdapterPosition();
            holder.renaming = false;
            holder.renameEdit.setOnFocusChangeListener(null);
            String suffix = String.valueOf(holder.renameSuffix.getText());
            String base = sanitizeRenamedBase(holder.renameEdit.getText().toString());
            if (position != RecyclerView.NO_POSITION && position < selectedItems.size()) {
                SelectedItem item = selectedItems.get(position);
                if (base.isEmpty()) base = editableFileBase(item.name);
                item.name = base + suffix;
                holder.name.setText((position + 1) + ". " + item.name);
            }
            holder.renameRow.setVisibility(View.GONE);
            holder.name.setVisibility(View.VISIBLE);
            holder.renameEdit.clearFocus();
            android.view.inputmethod.InputMethodManager keyboard =
                    (android.view.inputmethod.InputMethodManager) getSystemService(
                            android.content.Context.INPUT_METHOD_SERVICE);
            if (keyboard != null) keyboard.hideSoftInputFromWindow(
                    holder.renameEdit.getWindowToken(), 0);
        }

        @Override public int getItemCount() { return selectedItems.size(); }

        final class Holder extends RecyclerView.ViewHolder {
            final ImageView thumbnail;
            final TextView name;
            final LinearLayout renameRow;
            final EditText renameEdit;
            final TextView renameSuffix;
            final TextView detail;
            final TextView remove;
            boolean renaming;
            Holder(View itemView, ImageView thumbnail, TextView name,
                   LinearLayout renameRow, EditText renameEdit, TextView renameSuffix,
                   TextView detail, TextView remove) {
                super(itemView);
                this.thumbnail = thumbnail;
                this.name = name;
                this.renameRow = renameRow;
                this.renameEdit = renameEdit;
                this.renameSuffix = renameSuffix;
                this.detail = detail;
                this.remove = remove;
            }
        }
    }

    private void showVideoItemMenu(View anchor, int position) {
        if (busy || position < 0 || position >= selectedItems.size()) return;
        SelectedItem item = selectedItems.get(position);
        if (!item.isVideo()) return;
        PopupMenu popup = new PopupMenu(this, anchor);
        popup.getMenu().add("复制");
        popup.getMenu().add(item.reversed ? "取消倒放" : "倒放");
        popup.setOnMenuItemClickListener(menuItem -> {
            String title = String.valueOf(menuItem.getTitle());
            if ("复制".equals(title)) {
                SelectedItem copy = new SelectedItem(item.uri, item.name, item.mime,
                        item.size, item.sourceFormat, item.reversed, true);
                int insertAt = Math.min(selectedItems.size(), position + 1);
                selectedItems.add(insertAt, copy);
                animationEdits = freshAnimationEdits();
                selectedAdapter.notifyItemInserted(insertAt);
                selectedAdapter.notifyItemRangeChanged(insertAt,
                        selectedItems.size() - insertAt);
                updateSelectionUi();
                toast("已复制视频片段，可继续拖动调整顺序");
                return true;
            }
            if ("倒放".equals(title) || "取消倒放".equals(title)) {
                item.reversed = !item.reversed;
                animationEdits = freshAnimationEdits();
                selectedAdapter.notifyItemChanged(position);
                updateSelectionUi();
                toast(item.reversed ? "此视频片段将倒放" : "已恢复正向播放");
                return true;
            }
            return false;
        });
        popup.show();
    }

    private String sourceFormatLabel(SourceFormat format) {
        switch (format) {
            case JPEG: return "JPEG";
            case PNG: return "PNG";
            case BMP: return "BMP";
            case GIF: return "GIF";
            case WEBP: return "WebP";
            case HEIC: return "HEIC/HEIF";
            case VIDEO: return "视频";
            case PDF: return "PDF";
            case MARKDOWN: return "Markdown";
            case HTML: return "HTML";
            case CSV: return "CSV";
            case JSON: return "JSON";
            case TXT: return "文本";
            case OTHER_IMAGE: return "图片";
            default: return "文件";
        }
    }

    private String humanSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        double kb = bytes / 1024.0;
        if (kb < 1024) return String.format(Locale.CHINA, "%.1f KB", kb);
        double mb = kb / 1024.0;
        if (mb < 1024) return String.format(Locale.CHINA, "%.1f MB", mb);
        return String.format(Locale.CHINA, "%.2f GB", mb / 1024.0);
    }

    private enum SourceFormat {
        JPEG, PNG, BMP, GIF, WEBP, HEIC, VIDEO, PDF, OTHER_IMAGE,
        MARKDOWN, HTML, CSV, JSON, TXT, TSV, YAML, XML, SRT, VTT, DOCX, EPUB, ODT, RTF, FB2, JSONL, AUDIO, UNKNOWN
    }

    private static final class SelectedItem {
        final Uri uri;
        String name;
        final String mime;
        final long size;
        final SourceFormat sourceFormat;
        boolean reversed;
        final boolean copied;
        SelectedItem(Uri uri, String name, String mime, long size, SourceFormat sourceFormat) {
            this(uri, name, mime, size, sourceFormat, false, false);
        }
        SelectedItem(Uri uri, String name, String mime, long size, SourceFormat sourceFormat,
                     boolean reversed, boolean copied) {
            this.uri = uri;
            this.name = name;
            this.mime = mime;
            this.size = size;
            this.sourceFormat = sourceFormat;
            this.reversed = reversed;
            this.copied = copied;
        }
        boolean isVideo() { return sourceFormat == SourceFormat.VIDEO; }
    }

    private static final class ConversionSettings {
        final int resolutionPosition;
        final int customWidth;
        final int customHeight;
        final AnimationEdits edits;
        final int gifLoopCount;
        ConversionSettings(
                int resolutionPosition, int customWidth, int customHeight,
                AnimationEdits edits, int gifLoopCount) {
            this.gifLoopCount = gifLoopCount;
            this.resolutionPosition = resolutionPosition;
            this.customWidth = customWidth;
            this.customHeight = customHeight;
            this.edits = edits == null ? AnimationEdits.NONE : edits;
        }
    }

    private static final class ImageProfile {
        final double edgeStrength;
        final double contrast;

        ImageProfile(double edgeStrength, double contrast) {
            this.edgeStrength = edgeStrength;
            this.contrast = contrast;
        }
    }

    private static final class VideoSlice {
        final long startUs;
        final long endUs;
        final boolean reversed;

        VideoSlice(long startUs, long endUs, boolean reversed) {
            this.startUs = startUs;
            this.endUs = endUs;
            this.reversed = reversed;
        }
    }

    private static final class VideoTimeline {
        final List<SelectedItem> items = new ArrayList<>();
        final List<VideoFrameDecoder.Info> infos = new ArrayList<>();
        final List<Long> startsUs = new ArrayList<>();
        final List<Long> endsUs = new ArrayList<>();
        final List<Boolean> reversed = new ArrayList<>();
    }

    private static final class EditorTimelineState {
        final List<AnimationEdits.TimeRange> deletedRanges;
        final List<AnimationEdits.TimeRange> reversedRanges;
        final double splitPoint1;
        final double splitPoint2;

        EditorTimelineState(
                List<AnimationEdits.TimeRange> deletedRanges,
                List<AnimationEdits.TimeRange> reversedRanges,
                double splitPoint1, double splitPoint2) {
            this.deletedRanges = new ArrayList<>(deletedRanges);
            this.reversedRanges = new ArrayList<>(reversedRanges);
            this.splitPoint1 = splitPoint1;
            this.splitPoint2 = splitPoint2;
        }
    }

    private static String editorSplitStateText(double[] splitPoints) {
        if (splitPoints == null || splitPoints.length < 2
                || Double.isNaN(splitPoints[0])) {
            return "尚未设置分割点";
        }
        if (Double.isNaN(splitPoints[1])) {
            return String.format(Locale.CHINA,
                    "第 1 个分割点：%.2f 秒", splitPoints[0]);
        }
        return String.format(Locale.CHINA, "分割点：%.2f 秒、%.2f 秒",
                splitPoints[0], splitPoints[1]);
    }

    private static final class ActionState {
        final boolean enabled;
        final String label;
        final String reason;
        private ActionState(boolean enabled, String label, String reason) {
            this.enabled = enabled;
            this.label = label;
            this.reason = reason;
        }
        static ActionState enabled(String label, String reason) {
            return new ActionState(true, label, reason);
        }
        static ActionState disabled(String reason) {
            return new ActionState(false, "当前无需转换", reason);
        }
    }

    private static final class OutputSpec {
        final String extension;
        final String mime;
        final String shortName;
        OutputSpec(String extension, String mime, String shortName) {
            this.extension = extension;
            this.mime = mime;
            this.shortName = shortName;
        }
    }

    private enum BatchMode { SINGLE, SEPARATE, ZIP }

    private static final class PendingBatchFile {
        final File file;
        final String mime;
        final String fileName;
        PendingBatchFile(File file, String mime, String fileName) {
            this.file = file;
            this.mime = mime;
            this.fileName = fileName;
        }
    }

    private static final class BatchConversionResult {
        final List<PendingBatchFile> files;
        BatchConversionResult(List<PendingBatchFile> files) {
            this.files = files;
        }
    }

    private static final class ConversionResult {
        final File file;
        final String mime;
        final String fileName;
        ConversionResult(File file, String mime, String fileName) {
            this.file = file;
            this.mime = mime;
            this.fileName = fileName;
        }
    }

    private static final class CancelledException extends Exception {
        private static final long serialVersionUID = 1L;
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/Mp4Encoder.java': r'''package com.qi.formatconverter;

import android.graphics.Bitmap;
import android.media.MediaCodec;
import android.media.MediaCodecInfo;
import android.media.MediaCodecList;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import android.os.Build;
import android.view.Surface;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;

final class Mp4Encoder implements AutoCloseable {
    static final String MIME_H264 = "video/avc";
    static final String MIME_H265 = "video/hevc";
    static final String MIME_AV1 = "video/av01";
    private static final long TIMEOUT_US = 10_000;

    private final MediaCodec codec;
    private final MediaMuxer muxer;
    private final EglBitmapRenderer renderer;
    private final MediaCodec.BufferInfo bufferInfo = new MediaCodec.BufferInfo();
    private boolean muxerStarted;
    private int trackIndex = -1;
    private boolean closed;
    final int width;
    final int height;
    final int fps;
    final int bitrate;
    final String codecLabel;

    Mp4Encoder(
            File output,
            int requestedWidth,
            int requestedHeight,
            int requestedFps,
            int requestedBitrate,
            String mime,
            String codecLabel) throws IOException {
        this.codecLabel = codecLabel;
        fps = clamp(requestedFps, 1, 120);
        EncoderChoice choice = findEncoderAndSize(mime, requestedWidth, requestedHeight, fps);
        width = choice.width;
        height = choice.height;
        bitrate = requestedBitrate > 0
                ? clamp(requestedBitrate, 100_000, 120_000_000)
                : autoBitrate(mime, width, height, fps);

        MediaFormat format = MediaFormat.createVideoFormat(mime, width, height);
        format.setInteger(MediaFormat.KEY_COLOR_FORMAT,
                MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface);
        format.setInteger(MediaFormat.KEY_BIT_RATE, bitrate);
        format.setInteger(MediaFormat.KEY_FRAME_RATE, fps);
        format.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL, 1);

        MediaCodecInfo.CodecCapabilities capabilities = choice.info.getCapabilitiesForType(mime);
        MediaCodecInfo.EncoderCapabilities encoderCaps = capabilities.getEncoderCapabilities();
        if (encoderCaps.isBitrateModeSupported(
                MediaCodecInfo.EncoderCapabilities.BITRATE_MODE_VBR)) {
            format.setInteger(MediaFormat.KEY_BITRATE_MODE,
                    MediaCodecInfo.EncoderCapabilities.BITRATE_MODE_VBR);
        } else if (encoderCaps.isBitrateModeSupported(
                MediaCodecInfo.EncoderCapabilities.BITRATE_MODE_CBR)) {
            format.setInteger(MediaFormat.KEY_BITRATE_MODE,
                    MediaCodecInfo.EncoderCapabilities.BITRATE_MODE_CBR);
        }

        MediaCodec createdCodec = MediaCodec.createByCodecName(choice.info.getName());
        MediaMuxer createdMuxer = null;
        EglBitmapRenderer createdRenderer = null;
        Surface inputSurface = null;
        try {
            createdCodec.configure(
                    format, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE);
            inputSurface = createdCodec.createInputSurface();
            createdCodec.start();
            createdMuxer = new MediaMuxer(
                    output.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
            createdRenderer = new EglBitmapRenderer(inputSurface, width, height);
            inputSurface = null; // Ownership moved to the renderer.
        } catch (Throwable error) {
            if (createdRenderer != null) {
                try { createdRenderer.close(); } catch (Exception ignored) { }
            } else if (inputSurface != null) {
                try { inputSurface.release(); } catch (Exception ignored) { }
            }
            if (createdMuxer != null) {
                try { createdMuxer.release(); } catch (Exception ignored) { }
            }
            try { createdCodec.stop(); } catch (Exception ignored) { }
            try { createdCodec.release(); } catch (Exception ignored) { }
            throw new IOException(
                    codecLabel + " 编码器初始化失败：" + safeMessage(error), error);
        }
        codec = createdCodec;
        muxer = createdMuxer;
        renderer = createdRenderer;
    }

    void encodeFrame(Bitmap bitmap, long presentationTimeUs) {
        if (Thread.currentThread().isInterrupted()) throw new RuntimeException("转换已取消");
        renderer.draw(bitmap, presentationTimeUs * 1000L);
        drain(false);
    }

    void finish() {
        codec.signalEndOfInputStream();
        drain(true);
    }

    private void drain(boolean endOfStream) {
        int emptyPolls = 0;
        while (true) {
            if (Thread.currentThread().isInterrupted()) throw new RuntimeException("转换已取消");
            int status = codec.dequeueOutputBuffer(bufferInfo, endOfStream ? TIMEOUT_US : 0);
            if (status == MediaCodec.INFO_TRY_AGAIN_LATER) {
                if (!endOfStream) return;
                if (++emptyPolls > 500) {
                    throw new RuntimeException(codecLabel + " 编码器结束超时");
                }
            } else if (status == MediaCodec.INFO_OUTPUT_FORMAT_CHANGED) {
                if (muxerStarted) {
                    throw new RuntimeException("编码器重复改变输出格式");
                }
                trackIndex = muxer.addTrack(codec.getOutputFormat());
                muxer.start();
                muxerStarted = true;
                emptyPolls = 0;
            } else if (status >= 0) {
                emptyPolls = 0;
                ByteBuffer data = codec.getOutputBuffer(status);
                if (data == null) {
                    throw new RuntimeException("编码器输出缓冲区为空");
                }
                if ((bufferInfo.flags & MediaCodec.BUFFER_FLAG_CODEC_CONFIG) != 0) {
                    bufferInfo.size = 0;
                }
                if (bufferInfo.size > 0) {
                    if (!muxerStarted) {
                        throw new RuntimeException("MediaMuxer 尚未启动");
                    }
                    data.position(bufferInfo.offset);
                    data.limit(bufferInfo.offset + bufferInfo.size);
                    muxer.writeSampleData(trackIndex, data, bufferInfo);
                }
                codec.releaseOutputBuffer(status, false);
                if ((bufferInfo.flags & MediaCodec.BUFFER_FLAG_END_OF_STREAM) != 0) return;
            }
        }
    }

    private static EncoderChoice findEncoderAndSize(
            String mime, int requestedWidth, int requestedHeight, int fps) throws IOException {
        int width = makeEven(Math.max(16, requestedWidth));
        int height = makeEven(Math.max(16, requestedHeight));
        MediaCodecList list = new MediaCodecList(MediaCodecList.REGULAR_CODECS);

        int preferencePasses = Build.VERSION.SDK_INT >= 29 ? 2 : 1;
        for (int pass = 0; pass < preferencePasses; pass++) {
            EncoderChoice best = null;
            long bestArea = -1;
            for (MediaCodecInfo info : list.getCodecInfos()) {
                if (!info.isEncoder() || !supportsType(info, mime)) continue;
                if (Build.VERSION.SDK_INT >= 29) {
                    boolean wantHardware = pass == 0;
                    if (info.isHardwareAccelerated() != wantHardware) continue;
                }
                try {
                    MediaCodecInfo.CodecCapabilities caps = info.getCapabilitiesForType(mime);
                    if (!supportsSurfaceInput(caps)) continue;
                    MediaCodecInfo.VideoCapabilities video = caps.getVideoCapabilities();
                    int wAlign = Math.max(2, video.getWidthAlignment());
                    int hAlign = Math.max(2, video.getHeightAlignment());
                    int w = alignDown(width, wAlign);
                    int h = alignDown(height, hAlign);

                    for (int attempt = 0; attempt < 36 && w >= 16 && h >= 16; attempt++) {
                        try {
                            if (video.areSizeAndRateSupported(w, h, fps)) {
                                long area = (long) w * h;
                                if (area > bestArea) {
                                    best = new EncoderChoice(
                                            info, makeEven(w), makeEven(h));
                                    bestArea = area;
                                }
                                break;
                            }
                        } catch (IllegalArgumentException ignored) {
                        }
                        w = alignDown((int) Math.floor(w * 0.90), wAlign);
                        h = alignDown((int) Math.floor(h * 0.90), hAlign);
                    }
                } catch (Exception ignored) {
                }
            }
            if (best != null) return best;
        }
        throw new IOException("设备没有支持所选分辨率与帧率的 "
                + labelForMime(mime) + " Surface 编码器");
    }

    static boolean hasSurfaceEncoder(String mime) {
        MediaCodecList list = new MediaCodecList(MediaCodecList.REGULAR_CODECS);
        for (MediaCodecInfo info : list.getCodecInfos()) {
            if (!info.isEncoder() || !supportsType(info, mime)) continue;
            try {
                if (supportsSurfaceInput(info.getCapabilitiesForType(mime))) return true;
            } catch (Exception ignored) {
            }
        }
        return false;
    }

    private static boolean supportsType(MediaCodecInfo info, String mime) {
        for (String type : info.getSupportedTypes()) {
            if (mime.equalsIgnoreCase(type)) return true;
        }
        return false;
    }

    private static boolean supportsSurfaceInput(MediaCodecInfo.CodecCapabilities caps) {
        for (int color : caps.colorFormats) {
            if (color == MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface) return true;
        }
        return false;
    }

    static int autoBitrate(String mime, int width, int height, int fps) {
        double bitsPerPixelFrame;
        if (MIME_AV1.equals(mime)) bitsPerPixelFrame = 0.055;
        else if (MIME_H265.equals(mime)) bitsPerPixelFrame = 0.072;
        else bitsPerPixelFrame = 0.11;
        long value = Math.round(width * (double) height * fps * bitsPerPixelFrame);
        return (int) Math.max(450_000, Math.min(80_000_000L, value));
    }

    private static String labelForMime(String mime) {
        if (MIME_H265.equals(mime)) return "H.265/HEVC";
        if (MIME_AV1.equals(mime)) return "AV1";
        return "H.264/AVC";
    }

    private static String safeMessage(Throwable error) {
        String message = error.getMessage();
        return message == null || message.trim().isEmpty()
                ? error.getClass().getSimpleName() : message;
    }

    private static int alignDown(int value, int alignment) {
        int aligned = value - value % alignment;
        return Math.max(alignment, aligned);
    }

    private static int makeEven(int value) {
        return value % 2 == 0 ? value : value - 1;
    }

    private static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }

    @Override
    public void close() {
        if (closed) return;
        closed = true;
        try {
            renderer.close();
        } catch (Exception ignored) {
        }
        try {
            codec.stop();
        } catch (Exception ignored) {
        }
        try {
            codec.release();
        } catch (Exception ignored) {
        }
        try {
            if (muxerStarted) muxer.stop();
        } catch (Exception ignored) {
        }
        try {
            muxer.release();
        } catch (Exception ignored) {
        }
    }

    private static final class EncoderChoice {
        final MediaCodecInfo info;
        final int width;
        final int height;

        EncoderChoice(MediaCodecInfo info, int width, int height) {
            this.info = info;
            this.width = width;
            this.height = height;
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/PcmMath.java': r'''package com.qi.formatconverter;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.io.IOException;

/** Small bounded PCM operations shared by the audio pipeline and host tests. */
final class PcmMath {
    private PcmMath() { }
    static int sampleBytes(int encoding) throws IOException {
        switch (encoding) {
            case 3: return 1;
            case 2: return 2;
            case 21: return 3;
            case 4: case 22: return 4;
            default: throw new IOException("设备输出了不支持的 PCM 位深："+encoding);
        }
    }
    static float sample(ByteBuffer in, int encoding) {
        switch(encoding) {
            case 3: return ((in.get()&255)-128)/128f;
            case 4: { float f=in.getFloat(); return Float.isFinite(f)?Math.max(-1,Math.min(1,f)):0; }
            case 21: {int v=(in.get()&255)|((in.get()&255)<<8)|(in.get()<<16);return v/8388608f;}
            case 22: return (float)(in.getInt()/2147483648.0);
            default: return in.getShort()/32768f;
        }
    }
    static short clip(double v) { return (short)Math.max(-32768,Math.min(32767,Math.round(v))); }
    static ByteBuffer stereo(ByteBuffer input,int encoding,int channels,float[][] weights) throws IOException {
        input.order(ByteOrder.LITTLE_ENDIAN);
        int frameBytes=sampleBytes(encoding)*channels;
        if (channels<1||channels>32||input.remaining()%frameBytes!=0) throw new IOException("音频 PCM 帧不完整或声道数无效");
        ByteBuffer out=ByteBuffer.allocateDirect(input.remaining()/frameBytes*4).order(ByteOrder.nativeOrder());
        while(input.hasRemaining()) {
            double l=0,r=0;
            for(int ch=0;ch<channels;ch++){float v=sample(input,encoding);l+=v*weights[0][ch];r+=v*weights[1][ch];}
            out.putShort(clip(l*32768));out.putShort(clip(r*32768));
        }
        out.flip();return out;
    }
    static void reverseStereo(byte[] data,int length) {
        for(int a=0,b=length-4;a<b;a+=4,b-=4) for(int c=0;c<4;c++){byte t=data[a+c];data[a+c]=data[b+c];data[b+c]=t;}
    }
    static void mix(byte[] a,byte[] b,int length,double gainA,double gainB,long startFrame,long totalFrames,long fadeFrames) {
        for(int i=0;i<length;i+=4) {
            long frame=startFrame+i/4;
            double fade=fadeFrames<=0?1:Math.max(0,Math.min(1,Math.min(frame/(double)fadeFrames,(totalFrames-1-frame)/(double)fadeFrames)));
            for(int ch=0;ch<4;ch+=2){int p=i+ch;short x=(short)((a[p]&255)|(a[p+1]<<8));short y=(short)((b[p]&255)|(b[p+1]<<8));short v=clip((x*gainA+y*gainB)*fade);a[p]=(byte)v;a[p+1]=(byte)(v>>>8);}
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/PureJavaMp3Encoder.java': r'''package com.qi.formatconverter;

import co.ntbl.lame.mp3.Lame;
import co.ntbl.lame.mp3.LameGlobalFlags;
import co.ntbl.lame.mp3.MPEGMode;
import co.ntbl.lame.mp3.VbrMode;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;

/** A JNI-free streaming PCM-to-MP3 adapter around the Java LAME port. */
final class PureJavaMp3Encoder implements AutoCloseable {
    private static final int MAX_FRAMES_PER_ENCODE = 8_192;
    static final int PCM_16_BIT = 2;
    static final int PCM_8_BIT = 3;
    static final int PCM_FLOAT = 4;
    static final int PCM_24_BIT_PACKED = 21;
    static final int PCM_32_BIT = 22;

    private final OutputStream output;
    private final Lame lame;
    private final int inputChannels;
    private final int bytesPerSample;
    private final int pcmEncoding;
    private final int frameBytes;
    private final float[] leftWeights;
    private final float[] rightWeights;
    private final byte[] mp3Buffer = new byte[Lame.LAME_MAXMP3BUFFER];
    private byte[] pcmBuffer = new byte[64 * 1024];
    private float[] left = new float[0];
    private float[] right = new float[0];
    private int pendingBytes;
    private boolean finished;
    private boolean closed;
    private long writtenBytes;

    PureJavaMp3Encoder(
            OutputStream output, int sampleRate, int inputChannels,
            int pcmEncoding) throws IOException {
        this(output, sampleRate, inputChannels, pcmEncoding, 0);
    }

    PureJavaMp3Encoder(
            OutputStream output, int sampleRate, int inputChannels,
            int pcmEncoding, int channelMask) throws IOException {
        if (output == null) throw new NullPointerException("output == null");
        if (sampleRate < 8_000 || sampleRate > 192_000) {
            throw new IOException("不支持的音频采样率：" + sampleRate);
        }
        if (inputChannels < 1 || inputChannels > 32) {
            throw new IOException("不支持的音频声道数：" + inputChannels);
        }
        this.output = output;
        this.inputChannels = inputChannels;
        this.pcmEncoding = pcmEncoding;
        this.bytesPerSample = bytesPerSample(pcmEncoding);
        this.frameBytes = bytesPerSample * this.inputChannels;
        float[][] downmix = createDownmixWeights(this.inputChannels, channelMask);
        this.leftWeights = downmix[0];
        this.rightWeights = downmix[1];

        int outputChannels = this.inputChannels == 1 ? 1 : 2;
        lame = new Lame();
        LameGlobalFlags flags = lame.getFlags();
        flags.setInNumChannels(outputChannels);
        flags.setInSampleRate(sampleRate);
        flags.setMode(outputChannels == 1 ? MPEGMode.MONO : MPEGMode.JOINT_STEREO);
        flags.setVBR(VbrMode.vbr_off);
        flags.setBitRate(outputChannels == 1 ? 128 : 192);
        flags.setQuality(Lame.QUALITY_HIGH);
        lame.getId3().init(flags);
        flags.setWriteId3tagAutomatic(false);
        flags.setFindReplayGain(false);
        int result = lame.initParams();
        if (result < 0) {
            lame.close();
            throw new IOException("MP3 编码器初始化失败：" + result);
        }
    }

    long writtenBytes() {
        return writtenBytes;
    }

    void writePcm(ByteBuffer source) throws IOException {
        ensureOpen();
        if (source == null || !source.hasRemaining()) return;
        int incoming = source.remaining();
        ensurePcmCapacity(pendingBytes + incoming);
        source.get(pcmBuffer, pendingBytes, incoming);
        int available = pendingBytes + incoming;
        int usable = available - available % frameBytes;
        int encodedBytes = 0;
        while (encodedBytes < usable) {
            int chunkBytes = Math.min(
                    usable - encodedBytes,
                    MAX_FRAMES_PER_ENCODE * frameBytes);
            encodePcmBytes(encodedBytes, chunkBytes);
            encodedBytes += chunkBytes;
        }
        pendingBytes = available - usable;
        if (pendingBytes > 0) {
            System.arraycopy(pcmBuffer, usable, pcmBuffer, 0, pendingBytes);
        }
    }

    void finish() throws IOException {
        if (finished) return;
        ensureOpen();
        // A partial interleaved frame cannot represent every channel and is intentionally ignored.
        pendingBytes = 0;
        int encoded = lame.encodeFlush(mp3Buffer);
        if (encoded < 0) throw new IOException("MP3 编码收尾失败：" + encoded);
        if (encoded > 0) {
            output.write(mp3Buffer, 0, encoded);
            writtenBytes += encoded;
        }
        output.flush();
        finished = true;
    }

    private void encodePcmBytes(int inputOffset, int byteCount) throws IOException {
        int frames = byteCount / frameBytes;
        ensureSampleCapacity(frames);
        int offset = inputOffset;
        for (int frame = 0; frame < frames; frame++) {
            if (inputChannels == 1) {
                float value = readSample(offset);
                left[frame] = value;
                right[frame] = value;
                offset += bytesPerSample;
                continue;
            }
            double leftSum = 0.0;
            double rightSum = 0.0;
            for (int channel = 0; channel < inputChannels; channel++) {
                float value = readSample(offset);
                offset += bytesPerSample;
                leftSum += value * leftWeights[channel];
                rightSum += value * rightWeights[channel];
            }
            left[frame] = (float) leftSum;
            right[frame] = (float) rightSum;
        }

        int encoded = lame.encodeBuffer(left, right, frames, mp3Buffer);
        if (encoded < 0) throw new IOException("MP3 编码失败：" + encoded);
        if (encoded > 0) {
            output.write(mp3Buffer, 0, encoded);
            writtenBytes += encoded;
        }
    }

    private float readSample(int offset) throws IOException {
        switch (pcmEncoding) {
            case PCM_8_BIT:
                return ((pcmBuffer[offset] & 0xFF) - 128) * 16_777_216f;
            case PCM_FLOAT:
                float sample = Float.intBitsToFloat(readLittleEndianInt(offset));
                if (!Float.isFinite(sample)) return 0f;
                return Math.max(-1f, Math.min(1f, sample)) * 2_147_483_647f;
            case PCM_24_BIT_PACKED: {
                int value = (pcmBuffer[offset] & 0xFF)
                        | ((pcmBuffer[offset + 1] & 0xFF) << 8)
                        | ((pcmBuffer[offset + 2] & 0xFF) << 16);
                if ((value & 0x00800000) != 0) value |= 0xFF000000;
                return value * 256f;
            }
            case PCM_32_BIT:
                return readLittleEndianInt(offset);
            case PCM_16_BIT:
            default:
                int value = (pcmBuffer[offset] & 0xFF)
                        | (pcmBuffer[offset + 1] << 8);
                return ((short) value) * 65_536f;
        }
    }

    private int readLittleEndianInt(int offset) {
        return (pcmBuffer[offset] & 0xFF)
                | ((pcmBuffer[offset + 1] & 0xFF) << 8)
                | ((pcmBuffer[offset + 2] & 0xFF) << 16)
                | (pcmBuffer[offset + 3] << 24);
    }

    private void ensurePcmCapacity(int required) {
        if (pcmBuffer.length >= required) return;
        int capacity = pcmBuffer.length;
        while (capacity < required) capacity = Math.max(capacity + 1, capacity * 2);
        byte[] replacement = new byte[capacity];
        if (pendingBytes > 0) {
            System.arraycopy(pcmBuffer, 0, replacement, 0, pendingBytes);
        }
        pcmBuffer = replacement;
    }

    private void ensureSampleCapacity(int frames) {
        if (left.length >= frames) return;
        left = new float[frames];
        right = new float[frames];
    }

    private static int bytesPerSample(int encoding) throws IOException {
        if (encoding == PCM_8_BIT) return 1;
        if (encoding == PCM_16_BIT) return 2;
        if (encoding == PCM_24_BIT_PACKED) return 3;
        if (encoding == PCM_FLOAT || encoding == PCM_32_BIT) return 4;
        throw new IOException("不支持的 PCM 编码：" + encoding);
    }

    static float[][] createDownmixWeights(int channels, int channelMask) {
        float[] left = new float[channels];
        float[] right = new float[channels];
        if (channels == 1) {
            left[0] = right[0] = 1f;
            return new float[][]{left, right};
        }

        // Android interleaves channel-mask positions in ascending bit order.
        if (channelMask != 0 && Integer.bitCount(channelMask) == channels) {
            int channel = 0;
            for (int bit = 1; bit != 0 && channel < channels; bit <<= 1) {
                if ((channelMask & bit) == 0) continue;
                applyChannelWeight(bit, channel++, left, right);
            }
        } else {
            // Common PCM layouts when a vendor decoder omits KEY_CHANNEL_MASK.
            left[0] = 1f;
            right[1] = 1f;
            if (channels == 3) {
                left[2] = right[2] = 0.707f; // 3.0 center
            } else if (channels == 4) {
                left[2] = 0.707f;            // quad back-left
                right[3] = 0.707f;           // quad back-right
            } else if (channels >= 5) {
                left[2] = right[2] = 0.707f; // center
                int surroundStart = 3;
                if (channels >= 6) {
                    left[3] = right[3] = 0.35f; // LFE
                    surroundStart = 4;
                }
                for (int channel = surroundStart; channel < channels; channel++) {
                    if (((channel - surroundStart) & 1) == 0) left[channel] = 0.707f;
                    else right[channel] = 0.707f;
                }
            }
        }
        normalizeWeights(left);
        normalizeWeights(right);
        return new float[][]{left, right};
    }

    private static void applyChannelWeight(
            int bit, int channel, float[] left, float[] right) {
        switch (bit) {
            case 0x4: left[channel] = 1f; break;                       // front-left
            case 0x8: right[channel] = 1f; break;                      // front-right
            case 0x10: left[channel] = right[channel] = 0.707f; break; // center
            case 0x20: left[channel] = right[channel] = 0.35f; break;  // LFE
            case 0x40:                                                     // back-left
            case 0x100:
            case 0x800: left[channel] = 0.707f; break;                  // side-left
            case 0x80:                                                     // back-right
            case 0x200:
            case 0x1000: right[channel] = 0.707f; break;                // side-right
            case 0x400: left[channel] = right[channel] = 0.5f; break;   // back-center
            default:
                if ((channel & 1) == 0) left[channel] = 0.5f;
                else right[channel] = 0.5f;
        }
    }

    private static void normalizeWeights(float[] weights) {
        float total = 0f;
        for (float weight : weights) total += Math.abs(weight);
        if (total <= 1f) return;
        for (int i = 0; i < weights.length; i++) weights[i] /= total;
    }

    private void ensureOpen() {
        if (closed) throw new IllegalStateException("MP3 编码器已经关闭");
        if (finished) throw new IllegalStateException("MP3 编码已经结束");
    }

    @Override public void close() {
        if (closed) return;
        closed = true;
        lame.close();
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/SeamlessGifWriter.java': r'''package com.qi.formatconverter;

import java.io.IOException;
import java.util.Arrays;

/**
 * Small boundary-aware layer in front of {@link FastGifEncoder}.
 *
 * <p>Video encoders and animated-image timelines often contain two or three visually identical
 * frames at the beginning or end. Writing all of them gives an otherwise smooth GIF a tiny pause
 * every time it loops. Forward-to-reverse transitions also repeat the turning-point frame. This
 * class keeps only one indexed frame in flight, preserves normal middle timing, and trims a very
 * small number of near-identical boundary frames without buffering the whole animation. Repeated
 * frames in the middle are represented by one longer GIF delay, preserving the hold while avoiding
 * redundant palette/LZW work and reducing the output size.
 */
final class SeamlessGifWriter {
    private static final int MAX_EDGE_TRIM = 2;
    private static final int MAX_COMPARISON_SAMPLES = 4096;
    private static final double MAX_CHANGED_FRACTION = 0.08;
    private static final double MAX_MEAN_CHANNEL_DELTA = 3.0;

    private final FastGifEncoder encoder;
    private final int delayMs;
    private final int frameSize;
    private final byte[] pending;
    private final byte[] firstWritten;

    private int pendingCopies;
    private int writtenFrames;
    private int skippedBoundaryFrames;
    private boolean firstRun = true;
    private boolean atSegmentBoundary;
    private boolean pendingStartsSegment;
    private int boundaryDuplicateSkips;
    private boolean finished;

    SeamlessGifWriter(FastGifEncoder encoder, int delayMs) {
        if (encoder == null) throw new NullPointerException("encoder == null");
        this.encoder = encoder;
        this.delayMs = Math.max(10, delayMs);
        this.frameSize = encoder.pixelCount();
        this.pending = new byte[frameSize];
        this.firstWritten = new byte[frameSize];
    }

    /** Marks the next offered frame as the beginning of a video segment or repeated pass. */
    void markSegmentBoundary() {
        ensureNotFinished();
        if (pendingCopies > 0) {
            int trim = Math.min(MAX_EDGE_TRIM, Math.max(0, pendingCopies - 1));
            pendingCopies -= trim;
            skippedBoundaryFrames += trim;
            atSegmentBoundary = true;
            boundaryDuplicateSkips = 0;
        }
    }

    void offer(byte[] indexedFrame) throws IOException {
        ensureNotFinished();
        if (indexedFrame == null || indexedFrame.length < frameSize) {
            throw new IllegalArgumentException("GIF 索引帧尺寸不足");
        }

        if (pendingCopies == 0) {
            System.arraycopy(indexedFrame, 0, pending, 0, frameSize);
            pendingCopies = 1;
            pendingStartsSegment = firstRun || atSegmentBoundary;
            atSegmentBoundary = false;
            boundaryDuplicateSkips = 0;
            return;
        }

        // Similarity trimming is deliberately limited to an animation/segment edge. In the
        // middle, even a tiny moving object is real motion and only byte-identical frames may be
        // folded into a longer delay; this avoids turning subtle motion into visible stepping.
        boolean allowNearDuplicate = atSegmentBoundary
                && boundaryDuplicateSkips < MAX_EDGE_TRIM;
        boolean duplicate = allowNearDuplicate
                ? isNearDuplicate(pending, indexedFrame)
                : Arrays.equals(pending, indexedFrame);
        if (duplicate) {
            if (atSegmentBoundary && boundaryDuplicateSkips < MAX_EDGE_TRIM) {
                // The last frame of one segment and first frame of the next would otherwise stay
                // on screen for several delays. Keep the earlier copy and discard only the tiny
                // duplicated run at the boundary; a genuinely long still scene is preserved.
                skippedBoundaryFrames++;
                boundaryDuplicateSkips++;
            } else {
                pendingCopies++;
                atSegmentBoundary = false;
                boundaryDuplicateSkips = 0;
            }
            return;
        }

        boolean trimHead = firstRun || pendingStartsSegment;
        int copies = trimHead ? Math.max(1, pendingCopies - MAX_EDGE_TRIM) : pendingCopies;
        if (trimHead) skippedBoundaryFrames += pendingCopies - copies;
        flushPending(copies);
        firstRun = false;
        System.arraycopy(indexedFrame, 0, pending, 0, frameSize);
        pendingCopies = 1;
        pendingStartsSegment = atSegmentBoundary;
        atSegmentBoundary = false;
        boundaryDuplicateSkips = 0;
    }

    /** Writes the final pending run after removing only tiny head/tail and loop duplicates. */
    void finishFrames() throws IOException { finishFrames(true); }

    void finishFrames(boolean repeating) throws IOException {
        if (finished) return;
        finished = true;
        if (pendingCopies <= 0) return;

        if (firstRun) {
            int copies = Math.max(1, pendingCopies - MAX_EDGE_TRIM);
            skippedBoundaryFrames += pendingCopies - copies;
            flushPending(copies);
            return;
        }

        int copies = Math.max(1, pendingCopies - MAX_EDGE_TRIM);
        skippedBoundaryFrames += pendingCopies - copies;
        if (repeating && writtenFrames >= 2 && isNearDuplicate(pending, firstWritten)) {
            // The GIF player immediately displays firstWritten after pending. Removing one copy
            // prevents the same visual endpoint from occupying two consecutive frame delays.
            copies = Math.max(0, copies - 1);
            skippedBoundaryFrames++;
        }
        flushPending(copies);
    }

    int writtenFrames() {
        return writtenFrames;
    }

    int skippedBoundaryFrames() {
        return skippedBoundaryFrames;
    }

    private void flushPending(int copies) throws IOException {
        if (copies <= 0) {
            pendingCopies = 0;
            return;
        }
        if (writtenFrames == 0) {
            System.arraycopy(pending, 0, firstWritten, 0, frameSize);
        }
        int normalizedDelayMs = Math.max(10,
                Math.min(655_350, ((delayMs + 5) / 10) * 10));
        long remainingDelayMs = (long) normalizedDelayMs * copies;
        while (remainingDelayMs > 0) {
            int encodedDelayMs = (int) Math.min(655_350L, remainingDelayMs);
            encoder.addIndexedFrame(pending, encodedDelayMs);
            writtenFrames++;
            remainingDelayMs -= encodedDelayMs;
        }
        pendingCopies = 0;
    }

    private boolean isNearDuplicate(byte[] first, byte[] second) {
        int stride = Math.max(1, frameSize / MAX_COMPARISON_SAMPLES);
        int samples = 0;
        int changed = 0;
        long totalDelta = 0;
        for (int index = 0; index < frameSize; index += stride) {
            int a = first[index] & 0xFF;
            int b = second[index] & 0xFF;
            samples++;
            if (a == b) continue;

            int colorA = FastGifEncoder.paletteRgb(a);
            int colorB = FastGifEncoder.paletteRgb(b);
            int delta = Math.abs(((colorA >>> 16) & 0xFF) - ((colorB >>> 16) & 0xFF))
                    + Math.abs(((colorA >>> 8) & 0xFF) - ((colorB >>> 8) & 0xFF))
                    + Math.abs((colorA & 0xFF) - (colorB & 0xFF));
            totalDelta += delta;
            if (delta >= 32) changed++;
        }
        if (samples == 0) return Arrays.equals(first, second);
        double changedFraction = changed / (double) samples;
        double meanChannelDelta = totalDelta / (samples * 3.0);
        return changedFraction <= MAX_CHANGED_FRACTION
                && meanChannelDelta <= MAX_MEAN_CHANNEL_DELTA;
    }

    private void ensureNotFinished() {
        if (finished) throw new IllegalStateException("GIF 接缝处理已经结束");
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/SimplePdfWriter.java': r'''package com.qi.formatconverter;

import java.io.BufferedOutputStream;
import java.io.Closeable;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.List;
import java.util.Locale;
import java.util.function.BooleanSupplier;

/**
 * Minimal dependency-free PDF writer that assembles JPEG images into a PDF document.
 * Every JPEG becomes one page; pages use the image aspect ratio, so no letterboxing
 * is required. JPEG bytes are embedded directly through the DCTDecode filter, which
 * keeps the process fast and avoids a second lossy re-encode.
 *
 * <p>Pages are streamed to disk one at a time (constructor + writePage + finish),
 * so memory usage stays bounded to a single page regardless of document length.
 * The catalog, page tree and cross-reference table are written by {@link #finish()}.
 */
public final class SimplePdfWriter implements Closeable {

    /** Maximum side length of a PDF page in points (PDF specification limit is 14400). */
    private static final int MAX_PAGE_UNITS = 14400;

    /** One PDF page backed by a baseline JPEG (3 components, DeviceRGB). */
    public static final class Page {
        public final byte[] jpeg;
        public final int width;
        public final int height;

        public Page(byte[] jpeg, int width, int height) {
            if (jpeg == null || jpeg.length == 0) {
                throw new IllegalArgumentException("JPEG data is empty");
            }
            if (width <= 0 || height <= 0) {
                throw new IllegalArgumentException("Illegal page image size");
            }
            this.jpeg = jpeg;
            this.width = width;
            this.height = height;
        }
    }

    private final CountingOutput out;
    private final StringBuilder kids = new StringBuilder();
    private final LongList offsets = new LongList();
    private int pageCount = 0;
    private int nextObjectId = 4; // 1 = catalog, 2 = pages tree, 3 = info
    private boolean finished = false;
    private boolean failed = false;

    /** Opens the output file and writes the PDF header. */
    public SimplePdfWriter(File output) throws IOException {
        OutputStream raw = new BufferedOutputStream(
                new FileOutputStream(output), 256 * 1024);
        out = new CountingOutput(raw);
        writeAscii(out, "%PDF-1.4\n");
        // Binary comment so tools treat the file as binary (recommended by the spec).
        out.write(0x25);
        out.write(0xC7);
        out.write(0xEC);
        out.write(0x8F);
        out.write(0xA2);
        out.write('\n');
    }

    /** Appends one page built from a JPEG image. The page box keeps the image aspect. */
    public void writePage(byte[] jpeg, int width, int height) throws IOException {
        // Page box in points: 1 pixel -> 1 point, clamped to the PDF limit.
        double scale = Math.min(1.0d,
                MAX_PAGE_UNITS / (double) Math.max(width, height));
        int pageWidth = Math.max(1, (int) Math.round(width * scale));
        int pageHeight = Math.max(1, (int) Math.round(height * scale));
        writePage(jpeg, width, height, pageWidth, pageHeight);
    }

    /**
     * Appends one page with an explicit page box in points, letting the caller
     * render at a higher pixel resolution than the physical page size (e.g. a
     * 1190 x 1684 render on an A4 595 x 842 box for crisp text). The JPEG pixel
     * size is embedded as-is so no extra scaling happens.
     */
    public void writePage(byte[] jpeg, int width, int height,
                          int pageWidth, int pageHeight) throws IOException {
        if (finished) throw new IOException("PDF 已完成写入");
        if (failed) throw new IOException("PDF 写入已中断");
        if (jpeg == null || jpeg.length == 0) {
            throw new IOException("页面 JPEG 数据为空");
        }
        if (width <= 0 || height <= 0) {
            throw new IOException("页面图片尺寸非法");
        }
        if (pageWidth <= 0 || pageHeight <= 0 || pageWidth > MAX_PAGE_UNITS
                || pageHeight > MAX_PAGE_UNITS) {
            throw new IOException("页面尺寸超出 PDF 允许范围（1–" + MAX_PAGE_UNITS + "）");
        }
        int pageId = nextObjectId;
        int imageId = pageId + 1;
        int contentId = pageId + 2;
        nextObjectId += 3;
        pageCount++;

        if (pageCount > 1) kids.append(' ');
        kids.append(pageId).append(" 0 R");

        offsets.set(pageId, out.offset);
        writeAscii(out, pageId + " 0 obj\n<< /Type /Page /Parent 2 0 R "
                + "/MediaBox [0 0 " + pageWidth + " " + pageHeight + "] "
                + "/Resources << /XObject << /Im0 " + imageId
                + " 0 R >> /ProcSet [/PDF /ImageC] >> "
                + "/Contents " + contentId + " 0 R >>\nendobj\n");

        offsets.set(imageId, out.offset);
        writeAscii(out, imageId + " 0 obj\n<< /Type /XObject /Subtype /Image "
                + "/Width " + width + " /Height " + height
                + " /ColorSpace /DeviceRGB /BitsPerComponent 8 "
                + "/Filter /DCTDecode /Length " + jpeg.length + " >>\nstream\n");
        out.write(jpeg, 0, jpeg.length);
        writeAscii(out, "\nendstream\nendobj\n");

        String content = "q\n" + pageWidth + " 0 0 " + pageHeight
                + " 0 0 cm\n/Im0 Do\nQ\n";
        offsets.set(contentId, out.offset);
        writeAscii(out, contentId + " 0 obj\n<< /Length "
                + content.length() + " >>\nstream\n" + content + "endstream\nendobj\n");
    }

    /** Writes the document skeleton (catalog, page tree, info) and the xref table. */
    public void finish() throws IOException {
        if (finished) return;
        if (failed) throw new IOException("PDF 写入已中断");
        if (pageCount <= 0) {
            failed = true;
            throw new IOException("没有可写入的页面");
        }

        offsets.set(1, out.offset);
        writeAscii(out, "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n");
        offsets.set(2, out.offset);
        writeAscii(out, "2 0 obj\n<< /Type /Pages /Kids ["
                + kids + "] /Count " + pageCount + " >>\nendobj\n");
        offsets.set(3, out.offset);
        writeAscii(out, "3 0 obj\n<< /Producer (FormatConverter) >>\nendobj\n");

        long xrefOffset = out.offset;
        int objectCount = nextObjectId - 1;
        writeAscii(out, "xref\n0 " + (objectCount + 1) + "\n");
        writeAscii(out, "0000000000 65535 f\r\n");
        for (int i = 1; i <= objectCount; i++) {
            writeAscii(out, String.format(
                    Locale.ROOT, "%010d 00000 n\r\n", offsets.get(i)));
        }
        writeAscii(out, "trailer\n<< /Size " + (objectCount + 1)
                + " /Root 1 0 R /Info 3 0 R >>\nstartxref\n"
                + xrefOffset + "\n%%EOF\n");
        out.flush();
        out.close();
        finished = true;
    }

    /**
     * Closes the file. A half-written document (finish not reached) is left on disk
     * on purpose so the caller's error cleanup can delete it.
     */
    @Override public void close() {
        try {
            out.close();
        } catch (IOException ignored) { }
    }

    /** Convenience one-shot API used by tests and simple callers. */
    public static void write(
            File output, List<Page> pages, BooleanSupplier cancelled) throws IOException {
        try (SimplePdfWriter pdf = new SimplePdfWriter(output)) {
            for (Page page : pages) {
                if (cancelled != null && cancelled.getAsBoolean()) {
                    throw new IOException("任务已取消");
                }
                pdf.writePage(page.jpeg, page.width, page.height);
            }
            pdf.finish();
        }
    }

    private static void writeAscii(CountingOutput out, String value) throws IOException {
        byte[] bytes = value.getBytes("ISO-8859-1");
        out.write(bytes, 0, bytes.length);
    }

    /** Growable primitive long array for xref offsets, indexed by object id. */
    private static final class LongList {
        private long[] values = new long[64];
        private int size = 0;

        void ensure(int index) {
            if (index >= size) {
                size = index + 1;
            }
            if (index >= values.length) {
                int capacity = values.length;
                while (capacity <= index) capacity *= 2;
                long[] grown = new long[capacity];
                System.arraycopy(values, 0, grown, 0, values.length);
                values = grown;
            }
        }

        void set(int index, long value) {
            ensure(index);
            values[index] = value;
        }

        long get(int index) {
            if (index <= 0 || index >= size) {
                throw new IndexOutOfBoundsException("object id " + index);
            }
            return values[index];
        }
    }

    /** OutputStream wrapper that counts every byte written for xref offsets. */
    private static final class CountingOutput extends OutputStream {
        private final OutputStream out;
        long offset = 0;
        private boolean closed = false;

        CountingOutput(OutputStream out) {
            this.out = out;
        }

        @Override public void write(int oneByte) throws IOException {
            out.write(oneByte);
            offset++;
        }

        @Override public void write(byte[] buffer, int offset, int length) throws IOException {
            out.write(buffer, offset, length);
            this.offset += length;
        }

        @Override public void flush() throws IOException {
            if (!closed) out.flush();
        }

        @Override public void close() throws IOException {
            if (!closed) {
                closed = true;
                out.close();
            }
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/SubtitleKit.java': r'''package com.qi.formatconverter;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Pure-Java subtitle conversion between SubRip (SRT) and WebVTT with zero
 * third-party dependencies. Also builds plain-text transcripts and JSON cue
 * lists. Timestamps are accepted leniently (comma or dot milliseconds, 1-3
 * millisecond digits, optional hours for VTT) and always written canonically
 * (HH:MM:SS,mmm for SRT, HH:MM:SS.mmm for VTT). HTML-ish cue tags such as
 * {@code <c>} or {@code <v Speaker>} are stripped from all outputs.
 */
final class SubtitleKit {

    private SubtitleKit() { }

    /** One subtitle cue: sequential number, timing and text lines. */
    static final class Cue {
        final long startMs;
        final long endMs;
        final List<String> lines;

        Cue(long startMs, long endMs, List<String> lines) {
            this.startMs = startMs;
            this.endMs = endMs;
            this.lines = lines;
        }

        String text() {
            return String.join("\n", lines);
        }
    }

    private static final Pattern TIMESTAMP_LINE = Pattern.compile(
            "\\s*(\\d{1,2}):(\\d{1,2}):(\\d{1,2})(?:[,.](\\d{1,3}))?"
                    + "\\s*-->\\s*"
                    + "(\\d{1,2}):(\\d{1,2}):(\\d{1,2})(?:[,.](\\d{1,3}))?.*");

    private static final Pattern VTT_SHORT_TIMESTAMP = Pattern.compile(
            "\\s*(\\d{1,2}):(\\d{1,2})\\.(\\d{1,3})"
                    + "\\s*-->\\s*"
                    + "(\\d{1,2}):(\\d{1,2})\\.(\\d{1,3}).*");

    // ---------------------------------------------------------------------
    // Parsing
    // ---------------------------------------------------------------------

    /** Parses SRT text into cues. */
    public static List<Cue> parseSrt(String srt) {
        if (srt == null || srt.trim().isEmpty()) {
            throw new IllegalArgumentException("SRT 字幕内容为空");
        }
        String text = stripBom(srt);
        List<Block> blocks = splitBlocks(text);
        List<Cue> cues = new ArrayList<>();
        for (int b = 0; b < blocks.size(); b++) {
            List<String> lines = blocks.get(b).lines;
            cues.add(parseCueBlock(lines, b + 1, false));
        }
        if (cues.isEmpty()) {
            throw new IllegalArgumentException("SRT 中没有找到字幕块（需要 \"编号 + 时间轴 + 文本\"）");
        }
        return cues;
    }

    /** Parses WebVTT text into cues; header / NOTE / STYLE / REGION blocks are skipped. */
    public static List<Cue> parseVtt(String vtt) {
        if (vtt == null || vtt.trim().isEmpty()) {
            throw new IllegalArgumentException("WebVTT 字幕内容为空");
        }
        String text = stripBom(vtt);
        String[] rawLines = text.split("\n", -1);
        int headerIndex = -1;
        for (int i = 0; i < rawLines.length; i++) {
            String line = rawLines[i].trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("WEBVTT")) {
                headerIndex = i;
                break;
            }
            throw new IllegalArgumentException(
                    "WebVTT 文件缺少 \"WEBVTT\" 文件头（第一行应为 WEBVTT）");
        }
        if (headerIndex < 0) {
            throw new IllegalArgumentException("WebVTT 文件缺少 \"WEBVTT\" 文件头");
        }
        List<String> meaningful = new ArrayList<>();
        for (int i = headerIndex + 1; i < rawLines.length; i++) {
            meaningful.add(rawLines[i].endsWith("\r")
                    ? rawLines[i].substring(0, rawLines[i].length() - 1) : rawLines[i]);
        }
        List<Block> blocks = splitBlocks(String.join("\n", meaningful));
        List<Cue> cues = new ArrayList<>();
        int blockNumber = 0;
        for (Block block : blocks) {
            String first = block.lines.isEmpty() ? "" : block.lines.get(0).trim();
            if (first.startsWith("NOTE") || first.startsWith("STYLE")
                    || first.startsWith("REGION")) {
                continue;
            }
            blockNumber++;
            cues.add(parseCueBlock(block.lines, blockNumber, true));
        }
        if (cues.isEmpty()) {
            throw new IllegalArgumentException("WebVTT 中没有找到字幕块");
        }
        return cues;
    }

    private static String stripBom(String s) {
        return !s.isEmpty() && s.charAt(0) == '\uFEFF' ? s.substring(1) : s;
    }

    private static final class Block {
        final List<String> lines = new ArrayList<>();
    }

    private static List<Block> splitBlocks(String text) {
        List<Block> blocks = new ArrayList<>();
        String[] rawLines = text.replace("\r\n", "\n").replace('\r', '\n').split("\n", -1);
        Block current = null;
        for (String rawLine : rawLines) {
            if (rawLine.trim().isEmpty()) {
                if (current != null && !current.lines.isEmpty()) {
                    blocks.add(current);
                    current = null;
                }
                continue;
            }
            if (current == null) current = new Block();
            current.lines.add(rawLine);
        }
        if (current != null && !current.lines.isEmpty()) blocks.add(current);
        return blocks;
    }

    private static Cue parseCueBlock(List<String> lines, int blockNumber, boolean vtt) {
        int timelineIndex = -1;
        long startMs = -1;
        long endMs = -1;
        for (int i = 0; i < Math.min(2, lines.size()); i++) {
            Matcher matcher = TIMESTAMP_LINE.matcher(lines.get(i));
            if (matcher.matches()) {
                startMs = toMillis(matcher.group(1), matcher.group(2), matcher.group(3),
                        matcher.group(4));
                endMs = toMillis(matcher.group(5), matcher.group(6), matcher.group(7),
                        matcher.group(8));
                timelineIndex = i;
                break;
            }
            if (vtt) {
                Matcher shortMatcher = VTT_SHORT_TIMESTAMP.matcher(lines.get(i));
                if (shortMatcher.matches()) {
                    startMs = toMillis("0", shortMatcher.group(1), shortMatcher.group(2),
                            shortMatcher.group(3));
                    endMs = toMillis("0", shortMatcher.group(4), shortMatcher.group(5),
                            shortMatcher.group(6));
                    timelineIndex = i;
                    break;
                }
            }
        }
        if (timelineIndex < 0) {
            throw new IllegalArgumentException(
                    "字幕第 " + blockNumber + " 块缺少时间轴（需要 --> 格式的时间行）");
        }
        // An index line before the timeline is allowed (and ignored; output is renumbered).
        List<String> textLines = new ArrayList<>();
        for (int i = timelineIndex + 1; i < lines.size(); i++) {
            textLines.add(stripTags(lines.get(i)));
        }
        if (textLines.isEmpty()) {
            textLines.add("");
        }
        return new Cue(startMs, endMs, textLines);
    }

    private static long toMillis(String hours, String minutes, String seconds, String fraction) {
        long ms = 0;
        ms += Long.parseLong(hours) * 3600_000L;
        ms += Long.parseLong(minutes) * 60_000L;
        ms += Long.parseLong(seconds) * 1000L;
        if (fraction != null && !fraction.isEmpty()) {
            int digits = fraction.length();
            long value = Long.parseLong(fraction);
            while (digits < 3) {
                value *= 10;
                digits++;
            }
            ms += value;
        }
        return ms;
    }

    /** Removes VTT/HTML inline tags and decodes the basic entities. */
    static String stripTags(String line) {
        String result = line.replaceAll("<[^<>]*>", "");
        result = TextConverter.decodeHtmlEntities(result);
        return result;
    }

    // ---------------------------------------------------------------------
    // Writing
    // ---------------------------------------------------------------------

    /** Writes cues as SRT (renumbered from 1, comma milliseconds). */
    public static String writeSrt(List<Cue> cues) {
        StringBuilder sb = new StringBuilder();
        int index = 1;
        for (Cue cue : cues) {
            sb.append(index++).append('\n');
            sb.append(formatTimestamp(cue.startMs, true)).append(" --> ")
                    .append(formatTimestamp(cue.endMs, true)).append('\n');
            for (String line : cue.lines) {
                sb.append(stripTags(line)).append('\n');
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    /** Writes cues as WebVTT (WEBVTT header, dot milliseconds). */
    public static String writeVtt(List<Cue> cues) {
        StringBuilder sb = new StringBuilder();
        sb.append("WEBVTT\n\n");
        for (Cue cue : cues) {
            sb.append(formatTimestamp(cue.startMs, false)).append(" --> ")
                    .append(formatTimestamp(cue.endMs, false)).append('\n');
            for (String line : cue.lines) {
                sb.append(stripTags(line)).append('\n');
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    private static String formatTimestamp(long ms, boolean comma) {
        if (ms < 0) ms = 0;
        long totalSeconds = ms / 1000;
        int millis = (int) (ms % 1000);
        long hours = totalSeconds / 3600;
        long minutes = (totalSeconds % 3600) / 60;
        long seconds = totalSeconds % 60;
        return String.format("%02d:%02d:%02d%c%03d",
                hours, minutes, seconds, comma ? ',' : '.', millis);
    }

    // ---------------------------------------------------------------------
    // Other outputs
    // ---------------------------------------------------------------------

    /** Cue text only, one cue per paragraph — a readable transcript. */
    public static String toTranscript(List<Cue> cues) {
        StringBuilder sb = new StringBuilder();
        for (Cue cue : cues) {
            List<String> kept = new ArrayList<>();
            for (String line : cue.lines) {
                String stripped = stripTags(line).trim();
                if (!stripped.isEmpty()) kept.add(stripped);
            }
            if (!kept.isEmpty()) {
                sb.append(String.join("\n", kept)).append("\n\n");
            }
        }
        return sb.toString().trim();
    }

    /** Cues as a pretty JSON array (index / start / end / text). */
    public static String toJson(List<Cue> cues) {
        List<Object> array = new ArrayList<>();
        for (int i = 0; i < cues.size(); i++) {
            Cue cue = cues.get(i);
            Map<String, Object> object = new LinkedHashMap<>();
            object.put("index", i + 1);
            object.put("start", formatTimestamp(cue.startMs, true));
            object.put("end", formatTimestamp(cue.endMs, true));
            object.put("startMs", cue.startMs);
            object.put("endMs", cue.endMs);
            object.put("text", cue.text());
            array.add(object);
        }
        return TextConverter.writeJson(array, false);
    }

    // ---------------------------------------------------------------------
    // High-level conversions
    // ---------------------------------------------------------------------

    public static String srtToVtt(String srt) {
        return writeVtt(parseSrt(srt));
    }

    public static String vttToSrt(String vtt) {
        return writeSrt(parseVtt(vtt));
    }

    public static String srtToText(String srt) {
        return toTranscript(parseSrt(srt));
    }

    public static String vttToText(String vtt) {
        return toTranscript(parseVtt(vtt));
    }

    public static String srtToJson(String srt) {
        return toJson(parseSrt(srt));
    }

    public static String vttToJson(String vtt) {
        return toJson(parseVtt(vtt));
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/TextConverter.java': r'''package com.qi.formatconverter;

import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CodingErrorAction;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Pure-Java text format conversions with zero third-party dependencies:
 * Markdown -> TXT / HTML / CSV / TSV / JSON / YAML / XML (tables),
 * HTML -> TXT, CSV / TSV -> TXT / JSON / YAML / XML / MD / HTML,
 * JSON -> CSV / TSV / YAML / XML / MD / TXT / HTML, plus the YAML / XML /
 * subtitle hubs implemented by {@link YamlKit}, {@link XmlKit} and
 * {@link SubtitleKit}. All methods are static and safe to call from any thread.
 */
public final class TextConverter {

    private static final Charset UTF8 = Charset.forName("UTF-8");
    private static final Charset UTF16LE = Charset.forName("UTF-16LE");
    private static final Charset UTF16BE = Charset.forName("UTF-16BE");
    private static final Charset GB18030 = Charset.forName("GB18030");

    private TextConverter() { }

    // =========================================================================
    // Charset detection & decoding
    // =========================================================================

    /**
     * Decodes raw bytes into text: BOM first (UTF-8 / UTF-16LE / UTF-16BE),
     * then strict UTF-8, then GB18030 (superset of GBK) as a legacy fallback.
     */
    public static String decode(byte[] data) {
        if (data == null || data.length == 0) return "";
        if (data.length >= 3
                && (data[0] & 0xFF) == 0xEF && (data[1] & 0xFF) == 0xBB && (data[2] & 0xFF) == 0xBF) {
            return new String(data, 3, data.length - 3, UTF8);
        }
        if (data.length >= 2 && (data[0] & 0xFF) == 0xFF && (data[1] & 0xFF) == 0xFE) {
            return new String(data, 2, data.length - 2, UTF16LE);
        }
        if (data.length >= 2 && (data[0] & 0xFF) == 0xFE && (data[1] & 0xFF) == 0xFF) {
            return new String(data, 2, data.length - 2, UTF16BE);
        }
        try {
            CharsetDecoder decoder = UTF8.newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT);
            return decoder.decode(ByteBuffer.wrap(data)).toString();
        } catch (Exception notUtf8) {
            // GB18030 replaces malformed sequences instead of throwing.
            return new String(data, GB18030);
        }
    }

    // =========================================================================
    // CSV (RFC 4180 subset, lenient)
    // =========================================================================

    /** Parses CSV text into rows; accepts LF / CRLF record separators and quoted fields. */
    public static List<String[]> parseCsv(String csv) {
        List<String[]> rows = new ArrayList<>();
        if (csv == null || csv.isEmpty()) return rows;
        List<String> fields = new ArrayList<>();
        StringBuilder field = new StringBuilder();
        boolean inQuotes = false;
        int i = 0;
        int n = csv.length();
        while (i < n) {
            char c = csv.charAt(i);
            if (inQuotes) {
                if (c == '"') {
                    if (i + 1 < n && csv.charAt(i + 1) == '"') {
                        field.append('"');
                        i += 2;
                    } else {
                        inQuotes = false;
                        i++;
                    }
                } else {
                    field.append(c);
                    i++;
                }
                continue;
            }
            if (c == '"') {
                inQuotes = true;
                i++;
                continue;
            }
            if (c == ',') {
                fields.add(field.toString());
                field.setLength(0);
                i++;
                continue;
            }
            if (c == '\n' || c == '\r') {
                if (c == '\r' && i + 1 < n && csv.charAt(i + 1) == '\n') i += 2;
                else i++;
                fields.add(field.toString());
                field.setLength(0);
                rows.add(fields.toArray(new String[0]));
                fields = new ArrayList<>();
                continue;
            }
            field.append(c);
            i++;
        }
        if (field.length() > 0 || !fields.isEmpty()) {
            fields.add(field.toString());
            rows.add(fields.toArray(new String[0]));
        }
        return rows;
    }

    /** Writes rows as RFC 4180 CSV with CRLF line endings (Excel friendly). */
    public static String writeCsv(List<String[]> rows) {
        if (rows == null || rows.isEmpty()) return "";
        StringBuilder sb = new StringBuilder();
        for (String[] row : rows) {
            for (int c = 0; c < row.length; c++) {
                if (c > 0) sb.append(',');
                String value = row[c] == null ? "" : row[c];
                if (csvFieldNeedsQuote(value)) {
                    sb.append('"').append(value.replace("\"", "\"\"")).append('"');
                } else {
                    sb.append(value);
                }
            }
            sb.append("\r\n");
        }
        return sb.toString();
    }

    private static boolean csvFieldNeedsQuote(String value) {
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (c == ',' || c == '"' || c == '\n' || c == '\r') return true;
        }
        return false;
    }

    /** First row is the header; every following row becomes a JSON object. */
    public static String csvToJson(List<String[]> rows) {
        if (rows == null || rows.size() <= 1) return "[]";
        return writeJson(rowsToRecords(rows), false);
    }

    /** Header row + data rows as a list of ordered JSON-like records. */
    static List<Object> rowsToRecords(List<String[]> rows) {
        if (rows == null || rows.size() <= 1) return new ArrayList<>();
        String[] header = dedupeHeader(rows.get(0));
        List<Object> array = new ArrayList<>();
        for (int r = 1; r < rows.size(); r++) {
            String[] row = rows.get(r);
            Map<String, Object> object = new LinkedHashMap<>();
            for (int c = 0; c < header.length; c++) {
                object.put(header[c], c < row.length ? row[c] : "");
            }
            for (int c = header.length; c < row.length; c++) {
                object.put("列" + (c + 1), row[c]);
            }
            array.add(object);
        }
        return array;
    }

    private static String[] dedupeHeader(String[] header) {
        String[] result = new String[header.length];
        Map<String, Integer> seen = new LinkedHashMap<>();
        for (int i = 0; i < header.length; i++) {
            String name = header[i] == null ? "" : header[i].trim();
            if (name.isEmpty()) name = "列" + (i + 1);
            Integer count = seen.get(name);
            if (count == null) {
                seen.put(name, 1);
                result[i] = name;
            } else {
                int next = count + 1;
                seen.put(name, next);
                result[i] = name + "_" + next;
            }
        }
        return result;
    }

    /** Renders rows as an aligned plain-text table (CJK aware column widths). */
    public static String csvToTextTable(List<String[]> rows) {
        if (rows == null || rows.isEmpty()) return "";
        int cols = 0;
        for (String[] row : rows) cols = Math.max(cols, row.length);
        if (cols == 0) return "";
        int[] widths = new int[cols];
        for (String[] row : rows) {
            for (int c = 0; c < row.length; c++) {
                widths[c] = Math.max(widths[c], displayWidth(tableCell(row[c])));
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int r = 0; r < rows.size(); r++) {
            if (r == 1) sb.append(tableSeparator(widths));
            sb.append(tableRow(rows.get(r), widths, cols)).append('\n');
        }
        return sb.toString();
    }

    private static String tableSeparator(int[] widths) {
        StringBuilder sb = new StringBuilder("+");
        for (int width : widths) {
            for (int k = 0; k < width + 2; k++) sb.append('-');
            sb.append('+');
        }
        sb.append('\n');
        return sb.toString();
    }

    private static String tableRow(String[] row, int[] widths, int cols) {
        StringBuilder sb = new StringBuilder("|");
        for (int c = 0; c < cols; c++) {
            String cell = c < row.length ? tableCell(row[c]) : "";
            sb.append(' ').append(cell);
            int pad = widths[c] - displayWidth(cell);
            for (int k = 0; k < pad; k++) sb.append(' ');
            sb.append(" |");
        }
        return sb.toString();
    }

    private static String tableCell(String value) {
        if (value == null) return "";
        return value.replace("\r\n", "\\n").replace('\n', ' ').replace('\r', ' ').replace('\t', ' ');
    }

    /** Console display width: East-Asian wide/fullwidth characters count as 2. */
    public static int displayWidth(String s) {
        if (s == null || s.isEmpty()) return 0;
        int width = 0;
        int i = 0;
        while (i < s.length()) {
            int cp = s.codePointAt(i);
            width += codePointWidth(cp);
            i += Character.charCount(cp);
        }
        return width;
    }

    private static int codePointWidth(int cp) {
        if ((cp >= 0x1100 && cp <= 0x115F)
                || (cp >= 0x2E80 && cp <= 0x303E)
                || (cp >= 0x3041 && cp <= 0x33FF)
                || (cp >= 0x3400 && cp <= 0x4DBF)
                || (cp >= 0x4E00 && cp <= 0x9FFF)
                || (cp >= 0xA000 && cp <= 0xA4CF)
                || (cp >= 0xAC00 && cp <= 0xD7A3)
                || (cp >= 0xF900 && cp <= 0xFAFF)
                || (cp >= 0xFE30 && cp <= 0xFE4F)
                || (cp >= 0xFF00 && cp <= 0xFF60)
                || (cp >= 0xFFE0 && cp <= 0xFFE6)
                || (cp >= 0x20000 && cp <= 0x3FFFD)) {
            return 2;
        }
        return 1;
    }

    // =========================================================================
    // JSON (parser + writers)
    // =========================================================================

    /** Parses a JSON document; returns Map / List / String / Long / Double / Boolean / null. */
    public static Object parseJson(String json) {
        if (json == null) throw new IllegalArgumentException("JSON 内容为空");
        return new JsonParser(json).parseDocument();
    }

    /** Converts a top-level JSON array of objects (or arrays) into CSV text. */
    public static String jsonToCsv(String json) {
        return writeCsv(treeToRows(parseJson(json), "JSON"));
    }

    /** Converts a tree (List of Maps / Lists / scalars) into CSV rows. */
    static List<String[]> treeToRows(Object root, String sourceLabel) {
        if (!(root instanceof List)) {
            throw new IllegalArgumentException(sourceLabel
                    + " 顶层必须是数组（每行一个对象），当前是 " + jsonTypeName(root));
        }
        List<?> array = (List<?>) root;
        if (array.isEmpty()) {
            throw new IllegalArgumentException(sourceLabel + " 数组为空，没有可转换的数据行");
        }
        boolean allMaps = true;
        boolean allLists = true;
        for (Object element : array) {
            if (!(element instanceof Map)) allMaps = false;
            if (!(element instanceof List)) allLists = false;
        }
        List<String[]> rows = new ArrayList<>();
        if (allMaps) {
            Map<String, Integer> header = new LinkedHashMap<>();
            for (Object element : array) {
                for (Object key : ((Map<?, ?>) element).keySet()) {
                    if (!header.containsKey(key)) header.put((String) key, header.size());
                }
            }
            String[] headerRow = header.keySet().toArray(new String[0]);
            rows.add(headerRow);
            for (Object element : array) {
                Map<?, ?> map = (Map<?, ?>) element;
                String[] row = new String[header.size()];
                for (Map.Entry<?, ?> entry : map.entrySet()) {
                    String key = String.valueOf(entry.getKey());
                    Integer index = header.get(key);
                    if (index != null) row[index] = jsonCellText(entry.getValue());
                }
                rows.add(row);
            }
        } else if (allLists) {
            for (Object element : array) {
                List<?> list = (List<?>) element;
                String[] row = new String[list.size()];
                for (int c = 0; c < list.size(); c++) row[c] = jsonCellText(list.get(c));
                rows.add(row);
            }
        } else {
            for (Object element : array) {
                rows.add(new String[]{jsonCellText(element)});
            }
        }
        return rows;
    }

    private static String jsonTypeName(Object value) {
        if (value == null) return "null";
        if (value instanceof Map) return "对象";
        if (value instanceof List) return "数组";
        if (value instanceof String) return "字符串";
        return "数字或布尔值";
    }

    private static String jsonCellText(Object value) {
        if (value == null) return "";
        if (value instanceof String) return (String) value;
        if (value instanceof Boolean) return value.toString();
        if (value instanceof Double) return formatDouble((Double) value);
        if (value instanceof Number) return value.toString();
        return writeJson(value, true);
    }

    /** JSON writer with two-space indentation (or compact when {@code compact}). */
    public static String writeJson(Object value, boolean compact) {
        StringBuilder sb = new StringBuilder();
        writeJsonValue(value, sb, 0, compact);
        return sb.toString();
    }

    private static void writeJsonValue(Object value, StringBuilder sb, int indent, boolean compact) {
        if (value == null) {
            sb.append("null");
            return;
        }
        if (value instanceof String) {
            writeJsonString((String) value, sb);
            return;
        }
        if (value instanceof Boolean || value instanceof Long || value instanceof Integer) {
            sb.append(value.toString());
            return;
        }
        if (value instanceof Double) {
            sb.append(formatDouble((Double) value));
            return;
        }
        if (value instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) value;
            if (map.isEmpty()) {
                sb.append("{}");
                return;
            }
            sb.append(compact ? "{" : "{\n");
            boolean first = true;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (!first) sb.append(compact ? "," : ",\n");
                first = false;
                if (!compact) jsonIndent(sb, indent + 1);
                writeJsonString(String.valueOf(entry.getKey()), sb);
                sb.append(compact ? ":" : ": ");
                writeJsonValue(entry.getValue(), sb, indent + 1, compact);
            }
            if (!compact) {
                sb.append('\n');
                jsonIndent(sb, indent);
            }
            sb.append('}');
            return;
        }
        if (value instanceof List) {
            List<?> list = (List<?>) value;
            if (list.isEmpty()) {
                sb.append("[]");
                return;
            }
            sb.append(compact ? "[" : "[\n");
            boolean first = true;
            for (Object element : list) {
                if (!first) sb.append(compact ? "," : ",\n");
                first = false;
                if (!compact) jsonIndent(sb, indent + 1);
                writeJsonValue(element, sb, indent + 1, compact);
            }
            if (!compact) {
                sb.append('\n');
                jsonIndent(sb, indent);
            }
            sb.append(']');
            return;
        }
        writeJsonString(String.valueOf(value), sb);
    }

    private static void jsonIndent(StringBuilder sb, int level) {
        for (int i = 0; i < level; i++) sb.append("  ");
    }

    private static String formatDouble(double value) {
        if (Double.isNaN(value) || Double.isInfinite(value)) return "null";
        if (value == Math.floor(value) && Math.abs(value) < 1e15) {
            return Long.toString((long) value);
        }
        return Double.toString(value);
    }

    private static void writeJsonString(String s, StringBuilder sb) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                default:
                    if (c < 0x20) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
    }

    /** Strict recursive-descent JSON parser with a nesting-depth guard. */
    private static final class JsonParser {
        private final String s;
        private int pos;
        private int depth;

        JsonParser(String s) { this.s = s; }

        Object parseDocument() {
            skipWs();
            Object value = parseValue();
            skipWs();
            if (pos < s.length()) throw err("JSON 末尾有多余内容");
            return value;
        }

        private IllegalArgumentException err(String message) {
            return new IllegalArgumentException(message + "（位置 " + pos + "）");
        }

        private void skipWs() {
            while (pos < s.length()) {
                char c = s.charAt(pos);
                if (c == ' ' || c == '\t' || c == '\n' || c == '\r') pos++;
                else break;
            }
        }

        private char peek() {
            if (pos >= s.length()) throw err("JSON 意外结束");
            return s.charAt(pos);
        }

        private Object parseValue() {
            if (++depth > 256) throw err("JSON 嵌套层级过深");
            try {
                char c = peek();
                switch (c) {
                    case '{': return parseObject();
                    case '[': return parseArray();
                    case '"': return parseString();
                    case 't': expect("true"); return Boolean.TRUE;
                    case 'f': expect("false"); return Boolean.FALSE;
                    case 'n': expect("null"); return null;
                    default:
                        if (c == '-' || (c >= '0' && c <= '9')) return parseNumber();
                        throw err("JSON 无效字符 '" + c + "'");
                }
            } finally {
                depth--;
            }
        }

        private void expect(String word) {
            if (!s.startsWith(word, pos)) throw err("JSON 无效字面量");
            pos += word.length();
        }

        private Map<String, Object> parseObject() {
            pos++;
            Map<String, Object> map = new LinkedHashMap<>();
            skipWs();
            if (peek() == '}') {
                pos++;
                return map;
            }
            while (true) {
                skipWs();
                if (peek() != '"') throw err("JSON 对象键必须是字符串");
                String key = parseString();
                skipWs();
                if (peek() != ':') throw err("JSON 缺少冒号");
                pos++;
                skipWs();
                map.put(key, parseValue());
                skipWs();
                char c = peek();
                if (c == ',') {
                    pos++;
                    continue;
                }
                if (c == '}') {
                    pos++;
                    return map;
                }
                throw err("JSON 对象缺少逗号或右花括号");
            }
        }

        private List<Object> parseArray() {
            pos++;
            List<Object> list = new ArrayList<>();
            skipWs();
            if (peek() == ']') {
                pos++;
                return list;
            }
            while (true) {
                skipWs();
                list.add(parseValue());
                skipWs();
                char c = peek();
                if (c == ',') {
                    pos++;
                    continue;
                }
                if (c == ']') {
                    pos++;
                    return list;
                }
                throw err("JSON 数组缺少逗号或右方括号");
            }
        }

        private String parseString() {
            pos++;
            StringBuilder sb = new StringBuilder();
            while (true) {
                if (pos >= s.length()) throw err("JSON 字符串未闭合");
                char c = s.charAt(pos++);
                if (c == '"') return sb.toString();
                if (c == '\\') {
                    if (pos >= s.length()) throw err("JSON 转义未完成");
                    char escape = s.charAt(pos++);
                    switch (escape) {
                        case '"': sb.append('"'); break;
                        case '\\': sb.append('\\'); break;
                        case '/': sb.append('/'); break;
                        case 'b': sb.append('\b'); break;
                        case 'f': sb.append('\f'); break;
                        case 'n': sb.append('\n'); break;
                        case 'r': sb.append('\r'); break;
                        case 't': sb.append('\t'); break;
                        case 'u':
                            if (pos + 4 > s.length()) throw err("JSON \\u 转义不完整");
                            int code = 0;
                            for (int k = 0; k < 4; k++) {
                                char hex = s.charAt(pos++);
                                int digit = Character.digit(hex, 16);
                                if (digit < 0) throw err("JSON \\u 转义含非十六进制字符");
                                code = (code << 4) | digit;
                            }
                            sb.append((char) code);
                            break;
                        default:
                            throw err("JSON 无效转义 \\" + escape);
                    }
                } else if (c < 0x20) {
                    throw err("JSON 字符串包含未转义的控制字符");
                } else {
                    sb.append(c);
                }
            }
        }

        private Number parseNumber() {
            int start = pos;
            if (peek() == '-') pos++;
            while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            boolean integral = true;
            if (pos < s.length() && s.charAt(pos) == '.') {
                integral = false;
                pos++;
                if (pos >= s.length() || !Character.isDigit(s.charAt(pos))) {
                    throw err("JSON 小数缺少数字");
                }
                while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            }
            if (pos < s.length() && (s.charAt(pos) == 'e' || s.charAt(pos) == 'E')) {
                integral = false;
                pos++;
                if (pos < s.length() && (s.charAt(pos) == '+' || s.charAt(pos) == '-')) pos++;
                if (pos >= s.length() || !Character.isDigit(s.charAt(pos))) {
                    throw err("JSON 指数缺少数字");
                }
                while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            }
            String literal = s.substring(start, pos);
            if (literal.isEmpty() || literal.equals("-")) throw err("JSON 无效数字");
            try {
                if (integral) return Long.parseLong(literal);
                return Double.parseDouble(literal);
            } catch (NumberFormatException oversized) {
                return Double.parseDouble(literal);
            }
        }
    }

    // =========================================================================
    // HTML -> TXT
    // =========================================================================

    private static final Map<String, String> HTML_ENTITIES = buildHtmlEntities();

    private static Map<String, String> buildHtmlEntities() {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("amp", "&");
        map.put("lt", "<");
        map.put("gt", ">");
        map.put("quot", "\"");
        map.put("apos", "'");
        map.put("nbsp", " ");
        map.put("copy", "©");
        map.put("reg", "®");
        map.put("trade", "™");
        map.put("hellip", "…");
        map.put("mdash", "—");
        map.put("ndash", "–");
        map.put("lsquo", "‘");
        map.put("rsquo", "’");
        map.put("ldquo", "“");
        map.put("rdquo", "”");
        map.put("laquo", "«");
        map.put("raquo", "»");
        map.put("bull", "•");
        map.put("middot", "·");
        map.put("deg", "°");
        map.put("plus", "+");
        map.put("minus", "−");
        map.put("times", "×");
        map.put("divide", "÷");
        map.put("cent", "¢");
        map.put("pound", "£");
        map.put("yen", "¥");
        map.put("euro", "€");
        map.put("sect", "§");
        map.put("para", "¶");
        map.put("sup1", "¹");
        map.put("sup2", "²");
        map.put("sup3", "³");
        map.put("frac14", "¼");
        map.put("frac12", "½");
        map.put("frac34", "¾");
        map.put("dagger", "†");
        map.put("Dagger", "‡");
        map.put("permil", "‰");
        map.put("prime", "′");
        map.put("Prime", "″");
        map.put("check", "✓");
        map.put("star", "★");
        return map;
    }

    /** Strips tags, removes script/style, decodes entities and keeps readable line breaks. */
    public static String htmlToText(String html) {
        if (html == null || html.isEmpty()) return "";
        String s = html;
        s = s.replaceAll("(?is)<!--.*?-->", "");
        s = s.replaceAll("(?is)<(script|style)\\b[^>]*>.*?</\\1\\s*>", "");
        s = s.replaceAll("(?i)<br\\s*/?>", "\n");
        // Structural start tags open a new line.
        s = s.replaceAll("(?i)<(p|div|section|article|header|footer|main|aside|nav|blockquote|figure|figcaption|ul|ol|dl|table|thead|tbody|tr|pre|h[1-6])\\b[^>]*>", "\n");
        s = s.replaceAll("(?i)<li\\b[^>]*>", "\n- ");
        s = s.replaceAll("(?i)</(td|th)\\s*>", " | ");
        s = s.replaceAll("(?i)<(td|th)\\b[^>]*>", "");
        s = s.replaceAll("(?i)</(p|div|section|article|header|footer|main|aside|nav|blockquote|figure|figcaption|ul|ol|dl|dt|dd|li|table|thead|tbody|tr|caption|pre|h[1-6]|address|fieldset)\\s*>", "\n");
        // Strip any remaining well-formed tag (must start with a letter or /letter).
        s = s.replaceAll("(?i)</?[a-zA-Z][^>]*>", "");
        s = decodeHtmlEntities(s);
        return cleanupTextLines(s);
    }

    static String decodeHtmlEntities(String s) {
        if (s.indexOf('&') < 0) return s;
        StringBuilder sb = new StringBuilder(s.length());
        int i = 0;
        int n = s.length();
        while (i < n) {
            char c = s.charAt(i);
            if (c != '&') {
                sb.append(c);
                i++;
                continue;
            }
            int semi = s.indexOf(';', i + 1);
            if (semi < 0 || semi - i > 12) {
                sb.append(c);
                i++;
                continue;
            }
            String entity = s.substring(i + 1, semi);
            String replacement = null;
            if (!entity.isEmpty() && entity.charAt(0) == '#') {
                int code = -1;
                try {
                    if (entity.length() > 1 && (entity.charAt(1) == 'x' || entity.charAt(1) == 'X')) {
                        code = Integer.parseInt(entity.substring(2), 16);
                    } else {
                        code = Integer.parseInt(entity.substring(1));
                    }
                } catch (NumberFormatException ignored) { }
                if (code >= 0 && code <= 0x10FFFF
                        && !Character.isHighSurrogate((char) code)
                        && !Character.isLowSurrogate((char) code)) {
                    replacement = new String(Character.toChars(code));
                }
            } else {
                replacement = HTML_ENTITIES.get(entity);
            }
            if (replacement != null) {
                sb.append(replacement);
                i = semi + 1;
            } else {
                sb.append(c);
                i++;
            }
        }
        return sb.toString();
    }

    private static String cleanupTextLines(String s) {
        String[] lines = s.split("\n", -1);
        StringBuilder out = new StringBuilder();
        int blanks = 0;
        for (String raw : lines) {
            String line = raw.replaceAll("[ \\t\\x0B\\f\\r]+$", "").replaceAll("^[ \\t]+", "");
            while (line.endsWith("|")) {
                line = line.substring(0, line.length() - 1).replaceAll("[ \\t]+$", "");
            }
            if (line.isEmpty()) {
                blanks++;
                if (blanks <= 1 && out.length() > 0) out.append('\n');
            } else {
                blanks = 0;
                out.append(line).append('\n');
            }
        }
        return out.toString().trim();
    }

    // =========================================================================
    // Markdown block parsing
    // =========================================================================

    private static final class MdBlock {
        static final int HEADING = 0;
        static final int PARAGRAPH = 1;
        static final int CODE = 2;
        static final int QUOTE = 3;
        static final int LIST = 4;
        static final int TABLE = 5;
        static final int HR = 6;
        static final int HTML = 7;

        final int type;
        int level;                    // heading 1..6
        String text;                  // heading / paragraph raw text
        List<String> lines;           // code / html raw lines
        List<MdBlock> children;       // quote children
        boolean ordered;
        int listStart = 1;
        List<String> items;           // list item raw texts
        List<String[]> table;         // table rows (row 0 = header)
        int[] tableAlign;             // 0 left, 1 center, 2 right

        MdBlock(int type) { this.type = type; }
    }

    private static final Pattern FENCE_START = Pattern.compile("^(`{3,}|~{3,})\\s*\\S*\\s*$");
    private static final Pattern ATX_HEADING = Pattern.compile("^(#{1,6})(?:\\s+(.*?)|\\s*)$");
    private static final Pattern HR_LINE = Pattern.compile("^([-*_])\\s*(\\1\\s*){2,}$");
    private static final Pattern QUOTE_LINE = Pattern.compile("^\\s*>\\s?(.*)$");
    private static final Pattern BULLET_ITEM = Pattern.compile("^\\s*[-*+]\\s+(.+)$");
    private static final Pattern ORDERED_ITEM = Pattern.compile("^\\s*(\\d{1,9})[.)]\\s+(.+)$");
    private static final Pattern SETEXT_1 = Pattern.compile("^=+\\s*$");
    private static final Pattern SETEXT_2 = Pattern.compile("^-{2,}\\s*$");

    private static String stripSpaces(String line) {
        return line.replaceAll("^\\s+", "").replaceAll("\\s+$", "");
    }

    /** Parses markdown into a block list; handles fences, headings, quotes, lists, tables. */
    static List<MdBlock> parseMarkdownBlocks(String markdown) {
        String normalized = markdown.replace("\r\n", "\n").replace('\r', '\n');
        if (!normalized.isEmpty() && normalized.charAt(0) == '\uFEFF') {
            normalized = normalized.substring(1);
        }
        List<MdBlock> blocks = new ArrayList<>();
        String[] lines = normalized.split("\n", -1);
        int i = 0;
        int n = lines.length;
        while (i < n) {
            String line = lines[i];
            String trimmed = stripSpaces(line);
            if (trimmed.isEmpty()) {
                i++;
                continue;
            }
            // Fenced code block
            Matcher fence = FENCE_START.matcher(trimmed);
            if (fence.matches()) {
                String marker = fence.group(1);
                char fenceChar = marker.charAt(0);
                int fenceLength = marker.length();
                List<String> code = new ArrayList<>();
                i++;
                while (i < n) {
                    String candidate = stripSpaces(lines[i]);
                    if (isClosingFence(candidate, fenceChar, fenceLength)) {
                        i++;
                        break;
                    }
                    code.add(lines[i]);
                    i++;
                }
                MdBlock block = new MdBlock(MdBlock.CODE);
                block.lines = code;
                blocks.add(block);
                continue;
            }
            // ATX heading (requires whitespace or end-of-line after the hashes)
            Matcher atx = ATX_HEADING.matcher(trimmed);
            if (trimmed.startsWith("#") && atx.matches()) {
                MdBlock block = new MdBlock(MdBlock.HEADING);
                block.level = atx.group(1).length();
                String headingText = atx.group(2) == null ? "" : atx.group(2);
                block.text = headingText.replaceAll("\\s*#+\\s*$", "").trim();
                blocks.add(block);
                i++;
                continue;
            }
            // Horizontal rule
            if (HR_LINE.matcher(trimmed).matches()) {
                blocks.add(new MdBlock(MdBlock.HR));
                i++;
                continue;
            }
            // Blockquote
            Matcher quote = QUOTE_LINE.matcher(line);
            if (quote.matches()) {
                List<String> inner = new ArrayList<>();
                while (i < n) {
                    Matcher m = QUOTE_LINE.matcher(lines[i]);
                    if (m.matches()) {
                        inner.add(m.group(1));
                        i++;
                    } else if (stripSpaces(lines[i]).isEmpty()) {
                        // Blank line ends the quote.
                        break;
                    } else {
                        break;
                    }
                }
                MdBlock block = new MdBlock(MdBlock.QUOTE);
                block.children = parseMarkdownBlocks(String.join("\n", inner));
                blocks.add(block);
                continue;
            }
            // Table (header row + delimiter row)
            if (trimmed.indexOf('|') >= 0 && i + 1 < n) {
                String[] header = splitTableRow(trimmed);
                String[] delimiter = splitTableRow(stripSpaces(lines[i + 1]));
                if (isTableDelimiter(delimiter)) {
                    List<String[]> rows = new ArrayList<>();
                    rows.add(header);
                    int[] align = tableAlignment(delimiter);
                    i += 2;
                    while (i < n) {
                        String rowLine = stripSpaces(lines[i]);
                        if (rowLine.isEmpty() || rowLine.indexOf('|') < 0) break;
                        rows.add(splitTableRow(rowLine));
                        i++;
                    }
                    MdBlock block = new MdBlock(MdBlock.TABLE);
                    block.table = rows;
                    block.tableAlign = align;
                    blocks.add(block);
                    continue;
                }
            }
            // Lists
            Matcher bullet = BULLET_ITEM.matcher(line);
            Matcher ordered = ORDERED_ITEM.matcher(line);
            if (bullet.matches() || ordered.matches()) {
                boolean isOrdered = ordered.matches();
                int start = isOrdered ? Integer.parseInt(ordered.group(1)) : 1;
                List<String> items = new ArrayList<>();
                while (i < n) {
                    String itemLine = lines[i];
                    if (isOrdered) {
                        Matcher m = ORDERED_ITEM.matcher(itemLine);
                        if (!m.matches()) break;
                        items.add(m.group(2));
                    } else {
                        Matcher m = BULLET_ITEM.matcher(itemLine);
                        if (!m.matches()) break;
                        items.add(m.group(1));
                    }
                    i++;
                }
                MdBlock block = new MdBlock(MdBlock.LIST);
                block.ordered = isOrdered;
                block.listStart = start;
                block.items = items;
                blocks.add(block);
                continue;
            }
            // Raw HTML block
            if (trimmed.startsWith("<") && trimmed.length() > 1) {
                char next = trimmed.charAt(1);
                if (Character.isLetter(next) || next == '/' || next == '!') {
                    List<String> raw = new ArrayList<>();
                    while (i < n && !stripSpaces(lines[i]).isEmpty()) {
                        raw.add(lines[i]);
                        i++;
                    }
                    MdBlock block = new MdBlock(MdBlock.HTML);
                    block.lines = raw;
                    blocks.add(block);
                    continue;
                }
            }
            // Paragraph (with setext heading lookahead)
            List<String> para = new ArrayList<>();
            while (i < n) {
                String candidate = lines[i];
                String candidateTrim = stripSpaces(candidate);
                if (candidateTrim.isEmpty()) break;
                if (!para.isEmpty() && SETEXT_1.matcher(candidateTrim).matches()) {
                    MdBlock block = new MdBlock(MdBlock.HEADING);
                    block.level = 1;
                    block.text = String.join("\n", para).trim();
                    blocks.add(block);
                    i++;
                    para = null;
                    break;
                }
                if (!para.isEmpty() && SETEXT_2.matcher(candidateTrim).matches()) {
                    MdBlock block = new MdBlock(MdBlock.HEADING);
                    block.level = 2;
                    block.text = String.join("\n", para).trim();
                    blocks.add(block);
                    i++;
                    para = null;
                    break;
                }
                if (candidateTrim.startsWith("#") && ATX_HEADING.matcher(candidateTrim).matches()) break;
                if (candidateTrim.indexOf('|') >= 0 && i + 1 < n
                        && isTableDelimiter(splitTableRow(stripSpaces(lines[i + 1])))
                        && splitTableRow(candidateTrim).length > 1) break;
                if (FENCE_START.matcher(candidateTrim).matches()) break;
                if (QUOTE_LINE.matcher(candidate).matches()) break;
                if (HR_LINE.matcher(candidateTrim).matches()) break;
                if (BULLET_ITEM.matcher(candidate).matches()
                        || ORDERED_ITEM.matcher(candidate).matches()) break;
                if (candidateTrim.startsWith("<") && candidateTrim.length() > 1) {
                    char next = candidateTrim.charAt(1);
                    if (Character.isLetter(next) || next == '/' || next == '!') break;
                }
                para.add(candidate);
                i++;
            }
            if (para != null && !para.isEmpty()) {
                MdBlock block = new MdBlock(MdBlock.PARAGRAPH);
                block.text = String.join("\n", para);
                blocks.add(block);
            }
        }
        return blocks;
    }

    private static boolean isClosingFence(String candidate, char fenceChar, int minLength) {
        int count = 0;
        for (int i = 0; i < candidate.length(); i++) {
            if (candidate.charAt(i) == fenceChar) count++;
            else if (!Character.isWhitespace(candidate.charAt(i))) return false;
        }
        return count >= minLength;
    }

    private static String[] splitTableRow(String line) {
        String s = line.trim();
        if (s.startsWith("|")) s = s.substring(1);
        if (s.endsWith("|") && !s.endsWith("\\|")) s = s.substring(0, s.length() - 1);
        List<String> cells = new ArrayList<>();
        StringBuilder cell = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\\' && i + 1 < s.length() && s.charAt(i + 1) == '|') {
                cell.append('|');
                i++;
            } else if (c == '|') {
                cells.add(cell.toString().trim());
                cell.setLength(0);
            } else {
                cell.append(c);
            }
        }
        cells.add(cell.toString().trim());
        return cells.toArray(new String[0]);
    }

    private static boolean isTableDelimiter(String[] cells) {
        if (cells == null || cells.length == 0) return false;
        for (String cell : cells) {
            if (cell == null || !cell.matches("^:?-+:?$")) return false;
        }
        return true;
    }

    private static int[] tableAlignment(String[] delimiterCells) {
        int[] align = new int[delimiterCells.length];
        for (int i = 0; i < delimiterCells.length; i++) {
            String cell = delimiterCells[i];
            boolean left = cell.startsWith(":");
            boolean right = cell.endsWith(":") && cell.length() > 1;
            if (left && right) align[i] = 1;
            else if (right) align[i] = 2;
            else align[i] = 0;
        }
        return align;
    }

    // =========================================================================
    // Markdown -> HTML
    // =========================================================================

    private static final String HTML_CSS =
            "body{font-family:-apple-system,'Segoe UI',Roboto,'Noto Sans SC',sans-serif;"
                    + "max-width:820px;margin:40px auto;padding:0 20px;line-height:1.7;color:#222;}"
                    + "pre{background:#f6f8fa;padding:14px;border-radius:8px;overflow-x:auto;}"
                    + "code{font-family:Consolas,Menlo,monospace;background:#f6f8fa;"
                    + "padding:2px 5px;border-radius:4px;}"
                    + "pre code{padding:0;background:none;}"
                    + "blockquote{border-left:4px solid #d0d7de;margin:0 0 12px;"
                    + "padding:4px 18px;color:#57606a;background:#f6f8fa;}"
                    + "table{border-collapse:collapse;margin:14px 0;}"
                    + "th,td{border:1px solid #d0d7de;padding:7px 12px;}"
                    + "th{background:#f6f8fa;}"
                    + "img{max-width:100%;}"
                    + "hr{border:none;border-top:1px solid #d0d7de;}";

    /** Renders a complete standalone HTML page from markdown. */
    public static String markdownToHtml(String markdown, String title) {
        List<MdBlock> blocks = parseMarkdownBlocks(markdown);
        StringBuilder body = new StringBuilder();
        for (MdBlock block : blocks) {
            renderBlockHtml(block, body);
        }
        return "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n"
                + "<meta charset=\"utf-8\">\n"
                + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                + "<title>" + escapeHtml(title == null || title.trim().isEmpty()
                        ? "Markdown" : title.trim()) + "</title>\n"
                + "<style>" + HTML_CSS + "</style>\n"
                + "</head>\n<body>\n"
                + (body.length() == 0 ? "" : body.toString())
                + "</body>\n</html>\n";
    }

    private static void renderBlockHtml(MdBlock block, StringBuilder sb) {
        switch (block.type) {
            case MdBlock.HEADING:
                sb.append('<').append(headingTag(block.level)).append('>')
                        .append(renderInlineHtml(block.text))
                        .append("</").append(headingTag(block.level)).append(">\n");
                break;
            case MdBlock.PARAGRAPH:
                sb.append("<p>").append(renderInlineHtml(block.text)).append("</p>\n");
                break;
            case MdBlock.CODE:
                sb.append("<pre><code>")
                        .append(escapeHtml(String.join("\n", block.lines)))
                        .append("</code></pre>\n");
                break;
            case MdBlock.QUOTE:
                sb.append("<blockquote>\n");
                for (MdBlock child : block.children) renderBlockHtml(child, sb);
                sb.append("</blockquote>\n");
                break;
            case MdBlock.LIST:
                if (block.ordered) {
                    sb.append(block.listStart != 1
                            ? "<ol start=\"" + block.listStart + "\">\n" : "<ol>\n");
                } else {
                    sb.append("<ul>\n");
                }
                for (String item : block.items) {
                    sb.append("<li>").append(renderInlineHtml(item)).append("</li>\n");
                }
                sb.append(block.ordered ? "</ol>\n" : "</ul>\n");
                break;
            case MdBlock.TABLE:
                renderTableHtml(block, sb);
                break;
            case MdBlock.HR:
                sb.append("<hr>\n");
                break;
            case MdBlock.HTML:
                sb.append(String.join("\n", block.lines)).append('\n');
                break;
            default:
                break;
        }
    }

    private static String headingTag(int level) {
        return "h" + Math.max(1, Math.min(6, level));
    }

    private static void renderTableHtml(MdBlock block, StringBuilder sb) {
        List<String[]> rows = block.table;
        int[] align = block.tableAlign;
        sb.append("<table>\n<thead>\n<tr>");
        for (int c = 0; c < rows.get(0).length; c++) {
            sb.append("<th").append(alignAttr(align, c)).append('>')
                    .append(renderInlineHtml(rows.get(0)[c])).append("</th>");
        }
        sb.append("</tr>\n</thead>\n<tbody>\n");
        for (int r = 1; r < rows.size(); r++) {
            sb.append("<tr>");
            String[] row = rows.get(r);
            for (int c = 0; c < rows.get(0).length; c++) {
                String cell = c < row.length ? row[c] : "";
                sb.append("<td").append(alignAttr(align, c)).append('>')
                        .append(renderInlineHtml(cell)).append("</td>");
            }
            sb.append("</tr>\n");
        }
        sb.append("</tbody>\n</table>\n");
    }

    private static String alignAttr(int[] align, int column) {
        if (align == null || column >= align.length || align[column] == 0) return "";
        return " style=\"text-align:" + (align[column] == 1 ? "center" : "right") + "\"";
    }

    // =========================================================================
    // Markdown -> TXT
    // =========================================================================

    /** Renders markdown as clean plain text (syntax removed, structure kept readable). */
    public static String markdownToText(String markdown) {
        List<MdBlock> blocks = parseMarkdownBlocks(markdown);
        StringBuilder sb = new StringBuilder();
        for (MdBlock block : blocks) {
            renderBlockText(block, sb);
        }
        return sb.toString().trim();
    }

    private static void renderBlockText(MdBlock block, StringBuilder sb) {
        switch (block.type) {
            case MdBlock.HEADING: {
                String text = renderInlineText(block.text);
                sb.append(text).append('\n');
                int underline = Math.min(displayWidth(text), 60);
                if (block.level == 1) sb.append(repeatChar('=', underline)).append('\n');
                else if (block.level == 2) sb.append(repeatChar('-', underline)).append('\n');
                sb.append('\n');
                break;
            }
            case MdBlock.PARAGRAPH:
                sb.append(renderInlineText(block.text)).append("\n\n");
                break;
            case MdBlock.CODE:
                for (String line : block.lines) sb.append("    ").append(line).append('\n');
                sb.append('\n');
                break;
            case MdBlock.QUOTE: {
                StringBuilder inner = new StringBuilder();
                for (MdBlock child : block.children) renderBlockText(child, inner);
                String innerText = inner.toString().replaceAll("\n+$", "");
                for (String line : innerText.split("\n", -1)) {
                    sb.append(line.isEmpty() ? ">" : "> " + line).append('\n');
                }
                sb.append('\n');
                break;
            }
            case MdBlock.LIST: {
                int number = block.listStart;
                for (String item : block.items) {
                    sb.append(block.ordered ? (number + ". ") : "- ")
                            .append(renderInlineText(item)).append('\n');
                    number++;
                }
                sb.append('\n');
                break;
            }
            case MdBlock.TABLE:
                sb.append(csvToTextTable(block.table)).append('\n');
                break;
            case MdBlock.HR:
                sb.append(repeatChar('-', 10)).append("\n\n");
                break;
            case MdBlock.HTML:
                sb.append(htmlToText(String.join("\n", block.lines))).append("\n\n");
                break;
            default:
                break;
        }
    }

    private static String repeatChar(char c, int count) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) sb.append(c);
        return sb.toString();
    }

    // =========================================================================
    // Markdown table -> CSV
    // =========================================================================

    /** Extracts the first markdown table as rows (inline markup rendered). */
    public static List<String[]> markdownTableToRows(String markdown) {
        List<MdBlock> blocks = parseMarkdownBlocks(markdown);
        for (MdBlock block : blocks) {
            if (block.type == MdBlock.TABLE) {
                return markdownBlockToRows(block);
            }
            if (block.type == MdBlock.QUOTE) {
                for (MdBlock child : block.children) {
                    if (child.type == MdBlock.TABLE) {
                        return markdownBlockToRows(child);
                    }
                }
            }
        }
        throw new IllegalArgumentException("文档中没有找到 Markdown 表格（| 分隔的多行文本）");
    }

    private static List<String[]> markdownBlockToRows(MdBlock block) {
        List<String[]> rows = new ArrayList<>();
        for (String[] row : block.table) {
            String[] clean = new String[row.length];
            for (int c = 0; c < row.length; c++) clean[c] = renderInlineText(row[c]);
            rows.add(clean);
        }
        return rows;
    }

    /** Extracts the first markdown table and writes it as CSV. */
    public static String markdownTableToCsv(String markdown) {
        return writeCsv(markdownTableToRows(markdown));
    }

    // =========================================================================
    // Extended conversion hubs (TSV / YAML / XML / Markdown / HTML tables)
    // =========================================================================

    /** Parses TSV text (raw tab-separated values, one row per line). */
    public static List<String[]> parseTsv(String tsv) {
        List<String[]> rows = new ArrayList<>();
        if (tsv == null || tsv.isEmpty()) return rows;
        String normalized = tsv.replace("\r\n", "\n").replace('\r', '\n');
        String[] lines = normalized.split("\n", -1);
        for (int i = 0; i < lines.length; i++) {
            if (i == lines.length - 1 && lines[i].isEmpty()) break;
            rows.add(lines[i].split("\t", -1));
        }
        return rows;
    }

    /** Writes rows as TSV; cells cannot contain tabs/newlines so they are spaced. */
    public static String writeTsv(List<String[]> rows) {
        if (rows == null || rows.isEmpty()) return "";
        StringBuilder sb = new StringBuilder();
        for (String[] row : rows) {
            for (int c = 0; c < row.length; c++) {
                if (c > 0) sb.append('\t');
                sb.append(tsvCell(row[c]));
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    private static String tsvCell(String value) {
        if (value == null) return "";
        return value.replace("\r\n", " ").replace('\n', ' ')
                .replace('\r', ' ').replace('\t', ' ');
    }

    /** Renders rows as a Markdown table (header + delimiter row). */
    public static String rowsToMarkdownTable(List<String[]> rows) {
        if (rows == null || rows.isEmpty()) return "";
        int cols = 0;
        for (String[] row : rows) cols = Math.max(cols, row.length);
        if (cols == 0) return "";
        StringBuilder sb = new StringBuilder();
        for (int r = 0; r < rows.size(); r++) {
            String[] row = rows.get(r);
            sb.append('|');
            for (int c = 0; c < cols; c++) {
                String cell = c < row.length ? mdTableCell(row[c]) : "";
                sb.append(' ').append(cell).append(" |");
            }
            sb.append('\n');
            if (r == 0) {
                sb.append('|');
                for (int c = 0; c < cols; c++) sb.append(" --- |");
                sb.append('\n');
            }
        }
        return sb.toString();
    }

    private static String mdTableCell(String value) {
        if (value == null) return "";
        return value.replace("\r\n", " ").replace('\n', ' ')
                .replace('\r', ' ').replace('\t', ' ').replace("|", "\\|");
    }

    /** Renders rows as a standalone styled HTML table page. */
    public static String rowsToHtmlTablePage(List<String[]> rows, String title) {
        int cols = 0;
        if (rows != null) {
            for (String[] row : rows) cols = Math.max(cols, row.length);
        }
        StringBuilder body = new StringBuilder();
        body.append("<h1>").append(escapeHtml(title == null || title.trim().isEmpty()
                ? "表格数据" : title.trim())).append("</h1>\n");
        if (cols == 0) {
            body.append("<p>没有数据行。</p>\n");
        } else {
            body.append("<table>\n");
            if (rows.size() > 1) {
                body.append("<thead>\n<tr>");
                String[] header = rows.get(0);
                for (int c = 0; c < cols; c++) {
                    body.append("<th>").append(escapeHtml(c < header.length
                            ? header[c] : "")).append("</th>");
                }
                body.append("</tr>\n</thead>\n<tbody>\n");
            } else {
                body.append("<tbody>\n");
            }
            for (int r = 1; r < rows.size(); r++) {
                String[] row = rows.get(r);
                body.append("<tr>");
                for (int c = 0; c < cols; c++) {
                    body.append("<td>").append(escapeHtml(c < row.length
                            ? row[c] : "")).append("</td>");
                }
                body.append("</tr>\n");
            }
            body.append("</tbody>\n</table>\n");
        }
        return "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n"
                + "<meta charset=\"utf-8\">\n"
                + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                + "<title>" + escapeHtml(title == null || title.trim().isEmpty()
                ? "表格" : title.trim()) + "</title>\n"
                + "<style>" + HTML_CSS + "</style>\n"
                + "</head>\n<body>\n"
                + body
                + "</body>\n</html>\n";
    }

    // ---------------------------------------------------------------------
    // JSON hub extensions
    // ---------------------------------------------------------------------

    /** Pretty-prints JSON with two-space indentation. */
    public static String jsonToPrettyText(String json) {
        return writeJson(parseJson(json), false);
    }

    /** Renders pretty JSON inside a standalone HTML page. */
    public static String jsonToHtmlView(String json, String title) {
        String pretty = writeJson(parseJson(json), false);
        return "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n"
                + "<meta charset=\"utf-8\">\n"
                + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                + "<title>" + escapeHtml(title == null || title.trim().isEmpty()
                ? "JSON" : title.trim()) + "</title>\n"
                + "<style>" + HTML_CSS + "</style>\n"
                + "</head>\n<body>\n"
                + "<h1>" + escapeHtml(title == null || title.trim().isEmpty()
                ? "JSON" : title.trim()) + "</h1>\n"
                + "<pre>" + escapeHtml(pretty) + "</pre>\n"
                + "</body>\n</html>\n";
    }

    /** JSON array (of objects) as TSV. */
    public static String jsonToTsv(String json) {
        return writeTsv(treeToRows(parseJson(json), "JSON"));
    }

    /** Any JSON tree as block-style YAML. */
    public static String jsonToYaml(String json) {
        return YamlKit.write(parseJson(json));
    }

    /** Any JSON tree as a pretty XML document. */
    public static String jsonToXml(String json, String rootName) {
        return XmlKit.write(parseJson(json), rootName);
    }

    /** JSON array (of objects) as a Markdown table. */
    public static String jsonToMarkdown(String json) {
        return rowsToMarkdownTable(treeToRows(parseJson(json), "JSON"));
    }

    // ---------------------------------------------------------------------
    // YAML hub
    // ---------------------------------------------------------------------

    /** Parses YAML into the shared tree (Map / List / scalars). */
    public static Object yamlToTree(String yaml) {
        return YamlKit.parse(yaml);
    }

    /** YAML tree as pretty JSON. */
    public static String yamlToJson(String yaml) {
        return writeJson(YamlKit.parse(yaml), false);
    }

    /** YAML list-of-records as CSV. */
    public static String yamlToCsv(String yaml) {
        return writeCsv(treeToRows(YamlKit.parse(yaml), "YAML"));
    }

    /** YAML list-of-records as TSV. */
    public static String yamlToTsv(String yaml) {
        return writeTsv(treeToRows(YamlKit.parse(yaml), "YAML"));
    }

    /** YAML list-of-records as a Markdown table. */
    public static String yamlToMarkdown(String yaml) {
        return rowsToMarkdownTable(treeToRows(YamlKit.parse(yaml), "YAML"));
    }

    /** Any YAML tree as a pretty XML document. */
    public static String yamlToXml(String yaml, String rootName) {
        return XmlKit.write(YamlKit.parse(yaml), rootName);
    }

    // ---------------------------------------------------------------------
    // XML hub
    // ---------------------------------------------------------------------

    /** Parses XML and converts it to the shared tree (org.json conventions). */
    public static Object xmlToTree(String xml) {
        return XmlKit.toJsonValue(XmlKit.parseDocument(xml));
    }

    /** XML document as pretty JSON. */
    public static String xmlToJson(String xml) {
        return writeJson(xmlToTree(xml), false);
    }

    /** XML document as readable plain text (leaf texts, one per line). */
    public static String xmlToText(String xml) {
        return XmlKit.toPlainText(XmlKit.parseDocument(xml));
    }

    // ---------------------------------------------------------------------
    // TSV hub
    // ---------------------------------------------------------------------

    /** TSV as CSV. */
    public static String tsvToCsv(String tsv) {
        return writeCsv(parseTsv(tsv));
    }

    /** TSV as an aligned text table. */
    public static String tsvToTextTable(String tsv) {
        return csvToTextTable(parseTsv(tsv));
    }

    /** TSV as JSON records. */
    public static String tsvToJson(String tsv) {
        return writeJson(rowsToRecords(parseTsv(tsv)), false);
    }

    /** TSV as YAML records. */
    public static String tsvToYaml(String tsv) {
        return YamlKit.write(rowsToRecords(parseTsv(tsv)));
    }

    /** TSV as a Markdown table. */
    public static String tsvToMarkdown(String tsv) {
        return rowsToMarkdownTable(parseTsv(tsv));
    }

    /** TSV as a styled HTML table page. */
    public static String tsvToHtmlTablePage(String tsv, String title) {
        return rowsToHtmlTablePage(parseTsv(tsv), title);
    }

    /** TSV records as XML. */
    public static String tsvToXml(String tsv, String rootName) {
        return XmlKit.write(rowsToRecords(parseTsv(tsv)), rootName);
    }

    // ---------------------------------------------------------------------
    // CSV / Markdown table hub extensions
    // ---------------------------------------------------------------------

    /** CSV rows as a Markdown table. */
    public static String csvToMarkdown(List<String[]> rows) {
        return rowsToMarkdownTable(rows);
    }

    /** CSV rows as TSV. */
    public static String csvToTsv(List<String[]> rows) {
        return writeTsv(rows);
    }

    /** CSV rows as a styled HTML table page. */
    public static String csvToHtmlTablePage(List<String[]> rows, String title) {
        return rowsToHtmlTablePage(rows, title);
    }

    /** CSV rows as YAML records. */
    public static String csvToYaml(List<String[]> rows) {
        return YamlKit.write(rowsToRecords(rows));
    }

    /** CSV rows as XML records. */
    public static String csvToXml(List<String[]> rows, String rootName) {
        return XmlKit.write(rowsToRecords(rows), rootName);
    }

    /** Markdown table as TSV. */
    public static String markdownTableToTsv(String markdown) {
        return writeTsv(markdownTableToRows(markdown));
    }

    /** Markdown table as JSON records. */
    public static String markdownTableToJson(String markdown) {
        return writeJson(rowsToRecords(markdownTableToRows(markdown)), false);
    }

    /** Markdown table as YAML records. */
    public static String markdownTableToYaml(String markdown) {
        return YamlKit.write(rowsToRecords(markdownTableToRows(markdown)));
    }

    /** Markdown table as XML records. */
    public static String markdownTableToXml(String markdown, String rootName) {
        return XmlKit.write(rowsToRecords(markdownTableToRows(markdown)), rootName);
    }

    // =========================================================================
    // Inline rendering
    // =========================================================================

    private static final Pattern CODE_SPAN = Pattern.compile("(`+)([^`]|[^`][\\s\\S]*?[^`])\\1(?!`)");
    private static final Pattern BACKSLASH_ESCAPE =
            Pattern.compile("\\\\([\\\\`*_{}\\[\\]()#+\\-.!>~|])");
    private static final Pattern AUTOLINK = Pattern.compile("<(https?://|mailto:)[^\\s<>]+>");
    private static final Pattern IMAGE = Pattern.compile(
            "!\\[([^\\[\\]]*)\\]\\(\\s*(<[^>]*>|[^)\\s]+)(?:\\s+(?:\"([^\"]*)\"|&quot;([^&]*)&quot;))?\\s*\\)");
    private static final Pattern LINK = Pattern.compile(
            "\\[([^\\[\\]]+)\\]\\(\\s*(<[^>]*>|[^)\\s]+)(?:\\s+(?:\"([^\"]*)\"|&quot;([^&]*)&quot;))?\\s*\\)");
    private static final Pattern BOLD_ITALIC = Pattern.compile("\\*\\*\\*(.+?)\\*\\*\\*");
    private static final Pattern BOLD = Pattern.compile("\\*\\*(.+?)\\*\\*");
    private static final Pattern BOLD_UNDERSCORE = Pattern.compile("(?<!\\w)__(.+?)__(?!\\w)");
    private static final Pattern ITALIC = Pattern.compile("\\*(.+?)\\*");
    private static final Pattern ITALIC_UNDERSCORE = Pattern.compile("(?<!\\w)_(.+?)_(?!\\w)");
    private static final Pattern STRIKE = Pattern.compile("~~(.+?)~~");

    /** Placeholder marker for protected inline fragments (code spans, escapes, autolinks). */
    private static final char PROTECT = '\u0000';

    static String escapeHtml(String s) {
        if (s == null) return "";
        return s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }

    private static String renderInlineHtml(String text) {
        if (text == null || text.isEmpty()) return "";
        List<String> fragments = new ArrayList<>();
        List<Integer> fragmentTypes = new ArrayList<>();
        String s = protectCodeSpans(text, fragments, fragmentTypes);
        s = protectBackslashEscapes(s, fragments, fragmentTypes);
        s = protectAutolinks(s, fragments, fragmentTypes);
        s = escapeHtml(s);
        // Images first; the generated tag is protected so emphasis cannot corrupt the URL.
        s = IMAGE.matcher(s).replaceAll(match -> {
            String alt = match.group(1);
            String url = match.group(2);
            if (url != null && url.startsWith("&lt;") && url.endsWith("&gt;")) {
                url = url.substring(4, url.length() - 4);
            }
            String title = match.group(3) != null ? match.group(3) : match.group(4);
            String tag = "<img src=\"" + url + "\" alt=\"" + alt + "\""
                    + (title == null ? "" : " title=\"" + title + "\"") + ">";
            fragments.add(tag);
            fragmentTypes.add(PROTECT_RAW);
            return PROTECT_MARK + (fragments.size() - 1) + PROTECT_MARK;
        });
        s = applyEmphasis(s, true);
        // Links run last so their inner text already carries emphasis markup.
        s = LINK.matcher(s).replaceAll(match -> {
            String inner = match.group(1);
            String url = match.group(2);
            if (url != null && url.startsWith("&lt;") && url.endsWith("&gt;")) {
                url = url.substring(4, url.length() - 4);
            }
            String title = match.group(3) != null ? match.group(3) : match.group(4);
            return "<a href=\"" + url + "\"" + (title == null ? "" : " title=\"" + title + "\"")
                    + ">" + inner + "</a>";
        });
        return restoreProtected(s, fragments, fragmentTypes, true);
    }

    private static String renderInlineText(String text) {
        if (text == null || text.isEmpty()) return "";
        List<String> fragments = new ArrayList<>();
        List<Integer> fragmentTypes = new ArrayList<>();
        String s = protectCodeSpans(text, fragments, fragmentTypes);
        s = protectBackslashEscapes(s, fragments, fragmentTypes);
        s = protectAutolinks(s, fragments, fragmentTypes);
        s = IMAGE.matcher(s).replaceAll(match -> match.group(1));
        s = applyEmphasis(s, false);
        s = LINK.matcher(s).replaceAll(match -> match.group(1));
        return restoreProtected(s, fragments, fragmentTypes, false);
    }

    private static String applyEmphasis(String s, boolean html) {
        s = replace(BOLD_ITALIC, s, html ? "<strong><em>$1</em></strong>" : "$1");
        s = replace(BOLD, s, html ? "<strong>$1</strong>" : "$1");
        s = replace(BOLD_UNDERSCORE, s, html ? "<strong>$1</strong>" : "$1");
        s = replace(ITALIC, s, html ? "<em>$1</em>" : "$1");
        s = replace(ITALIC_UNDERSCORE, s, html ? "<em>$1</em>" : "$1");
        s = replace(STRIKE, s, html ? "<del>$1</del>" : "$1");
        return s;
    }

    private static String replace(Pattern pattern, String s, String replacement) {
        String result = pattern.matcher(s).replaceAll(replacement);
        return result;
    }

    private static final String PROTECT_MARK = String.valueOf(PROTECT);

    private static final int PROTECT_CODE = 0;
    private static final int PROTECT_CHAR = 1;
    private static final int PROTECT_URL = 2;
    private static final int PROTECT_RAW = 3;

    private static void addProtected(List<String> fragments, List<Integer> types,
                                     String value, int type, StringBuilder replacement) {
        fragments.add(value);
        types.add(type);
        replacement.append(PROTECT_MARK).append(fragments.size() - 1).append(PROTECT_MARK);
    }

    private static String protectCodeSpans(String text, List<String> fragments,
                                           List<Integer> types) {
        Matcher matcher = CODE_SPAN.matcher(text);
        StringBuilder sb = new StringBuilder();
        StringBuilder token = new StringBuilder();
        while (matcher.find()) {
            String content = matcher.group(2);
            // CommonMark: strip one leading and trailing space when both are present.
            if (content.length() >= 2 && content.charAt(0) == ' '
                    && content.charAt(content.length() - 1) == ' ') {
                content = content.substring(1, content.length() - 1);
            }
            token.setLength(0);
            addProtected(fragments, types, content, PROTECT_CODE, token);
            matcher.appendReplacement(sb, Matcher.quoteReplacement(token.toString()));
        }
        matcher.appendTail(sb);
        return sb.toString();
    }

    private static String protectBackslashEscapes(String text, List<String> fragments,
                                                   List<Integer> types) {
        Matcher matcher = BACKSLASH_ESCAPE.matcher(text);
        StringBuilder sb = new StringBuilder();
        StringBuilder token = new StringBuilder();
        while (matcher.find()) {
            token.setLength(0);
            addProtected(fragments, types, matcher.group(1), PROTECT_CHAR, token);
            matcher.appendReplacement(sb, Matcher.quoteReplacement(token.toString()));
        }
        matcher.appendTail(sb);
        return sb.toString();
    }

    private static String protectAutolinks(String text, List<String> fragments,
                                            List<Integer> types) {
        Matcher matcher = AUTOLINK.matcher(text);
        StringBuilder sb = new StringBuilder();
        StringBuilder token = new StringBuilder();
        while (matcher.find()) {
            String url = matcher.group(0);
            url = url.substring(1, url.length() - 1);
            token.setLength(0);
            addProtected(fragments, types, url, PROTECT_URL, token);
            matcher.appendReplacement(sb, Matcher.quoteReplacement(token.toString()));
        }
        matcher.appendTail(sb);
        return sb.toString();
    }

    private static String restoreProtected(String s, List<String> fragments,
                                           List<Integer> types, boolean html) {
        if (fragments.isEmpty()) return s;
        StringBuilder sb = new StringBuilder(s.length() + 32);
        int i = 0;
        int n = s.length();
        while (i < n) {
            if (s.charAt(i) == PROTECT) {
                int end = s.indexOf(PROTECT, i + 1);
                if (end > i) {
                    try {
                        int id = Integer.parseInt(s.substring(i + 1, end));
                        String value = fragments.get(id);
                        int type = types.get(id);
                        if (!html || type == PROTECT_RAW) {
                            sb.append(value);
                        } else if (type == PROTECT_CODE) {
                            sb.append("<code>").append(escapeHtml(value)).append("</code>");
                        } else if (type == PROTECT_URL) {
                            sb.append("<a href=\"").append(escapeHtml(value))
                                    .append("\">").append(escapeHtml(value)).append("</a>");
                        } else {
                            sb.append(escapeHtml(value));
                        }
                    } catch (Exception invalid) {
                        sb.append(s, i, end + 1);
                    }
                    i = end + 1;
                    continue;
                }
            }
            sb.append(s.charAt(i));
            i++;
        }
        return sb.toString();
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/TextPager.java': r'''package com.qi.formatconverter;

import java.util.ArrayList;
import java.util.List;

/**
 * Pure-Java text pagination for the text-to-PDF feature. The layout math is
 * platform independent: the caller supplies a {@link LineMeasurer} so host-JVM
 * tests can validate wrapping with a fake measurer while the app measures with
 * android.graphics.Paint. Pages use PostScript points (A4 = 595 x 842).
 *
 * <p>Wrapping rules: paragraphs are split on line breaks; each paragraph is
 * wrapped greedily by words when it contains spaces (Latin style) and by
 * characters when it has none (CJK style); a single word wider than the whole
 * content width is hard-split by characters so output can never overflow.
 */
public final class TextPager {

    /** Measures the rendered width of a line in points. */
    public interface LineMeasurer {
        float measureWidth(String line);
    }

    /** One paginated page: the lines to draw, in order. */
    public static final class Page {
        public final List<String> lines;

        Page(List<String> lines) {
            this.lines = lines;
        }
    }

    private TextPager() { }

    /** A4 portrait in PostScript points. */
    public static final float A4_WIDTH = 595f;
    public static final float A4_HEIGHT = 842f;

    /**
     * Paginates text into pages.
     *
     * @param text            the full document text (line breaks are respected)
     * @param measurer        width measurer in points (e.g. Paint::measureText)
     * @param pageWidth       page width in points
     * @param pageHeight      page height in points
     * @param marginX         left/right margins in points
     * @param marginTop       top margin in points
     * @param marginBottom    bottom margin in points
     * @param fontSize        body font size in points
     * @param lineHeightFactor line height as a multiple of the font size
     * @param maxPages        hard page-count guard
     * @param footerReserve   extra space reserved at the bottom for the page number
     */
    public static List<Page> paginate(String text, LineMeasurer measurer,
                                      float pageWidth, float pageHeight,
                                      float marginX, float marginTop, float marginBottom,
                                      float fontSize, float lineHeightFactor,
                                      int maxPages, float footerReserve) {
        if (text == null || text.trim().isEmpty()) {
            throw new IllegalArgumentException("文本内容为空，无法生成 PDF");
        }
        if (maxPages <= 0) throw new IllegalArgumentException("页数上限必须大于 0");
        float contentWidth = pageWidth - marginX * 2;
        if (contentWidth <= fontSize) {
            throw new IllegalArgumentException("页面宽度不足以排版文本");
        }
        float contentHeight = pageHeight - marginTop - marginBottom - footerReserve;
        float lineHeight = fontSize * lineHeightFactor;
        if (contentHeight < lineHeight * 2) {
            throw new IllegalArgumentException("页面高度不足以排版文本");
        }
        int linesPerPage = (int) Math.floor(contentHeight / lineHeight);

        // Normalize line endings, then split into paragraphs (source lines).
        String normalized = text.replace("\r\n", "\n").replace('\r', '\n');
        String[] sourceLines = normalized.split("\n", -1);

        List<String> allLines = new ArrayList<>();
        for (String sourceLine : sourceLines) {
            if (Thread.currentThread().isInterrupted()) throw new java.util.concurrent.CancellationException("已取消排版");
            if (allLines.size() > (long) maxPages * linesPerPage + 1)
                throw new IllegalArgumentException("文本超过页数上限，请拆分后转换");
            if (sourceLine.trim().isEmpty()) {
                allLines.add("");
                continue;
            }
            wrapLine(sourceLine, measurer, contentWidth, allLines);
        }

        // Drop blank lines before the first content and after the last content.
        int first = 0;
        while (first < allLines.size() && allLines.get(first).isEmpty()) first++;
        int last = allLines.size() - 1;
        while (last >= first && allLines.get(last).isEmpty()) last--;
        if (first > last) {
            throw new IllegalArgumentException("文本内容为空，无法生成 PDF");
        }
        List<String> body = allLines.subList(first, last + 1);

        List<Page> pages = new ArrayList<>();
        for (int i = 0; i < body.size(); i += linesPerPage) {
            if (pages.size() >= maxPages) {
                throw new IllegalArgumentException(
                        "内容过长：超过 " + maxPages + " 页上限，请拆分文件后再转换");
            }
            int end = Math.min(body.size(), i + linesPerPage);
            List<String> pageLines = new ArrayList<>(body.subList(i, end));
            pages.add(new Page(pageLines));
        }
        if (pages.isEmpty()) {
            throw new IllegalArgumentException("文本内容为空，无法生成 PDF");
        }
        return pages;
    }

    /** Greedy word wrap (Latin) with character fallback for CJK / overlong words. */
    private static void wrapLine(String line, LineMeasurer measurer,
                                 float contentWidth, List<String> out) {
        boolean hasSpaces = line.indexOf(' ') >= 0;
        if (!hasSpaces) {
            wrapByCharacters(line, measurer, contentWidth, out);
            return;
        }
        String[] words = line.split(" ", -1);
        StringBuilder current = new StringBuilder(256);
        for (int i = 0; i < words.length; i++) {
            String word = words[i];
            String candidate = current.length() == 0 ? word
                    : current + " " + word;
            if (measurer.measureWidth(candidate) <= contentWidth || current.length() == 0) {
                if (current.length() == 0) {
                    if (measurer.measureWidth(word) <= contentWidth) {
                        current.append(word);
                    } else {
                        // Single word wider than the line: hard-split it.
                        if (current.length() > 0) {
                            out.add(current.toString());
                            current.setLength(0);
                        }
                        wrapByCharacters(word, measurer, contentWidth, out, current);
                    }
                } else {
                    current.append(' ').append(word);
                }
            } else {
                out.add(current.toString());
                current.setLength(0);
                i--; // re-try this word at the start of the next line
            }
        }
        if (current.length() > 0) {
            out.add(current.toString());
        }
    }

    private static void wrapByCharacters(String line, LineMeasurer measurer,
                                         float contentWidth, List<String> out) {
        StringBuilder current = new StringBuilder(256);
        wrapByCharacters(line, measurer, contentWidth, out, current);
        if (current.length() > 0) out.add(current.toString());
    }

    /** Shared character-level greedy wrapper; leftover stays in {@code current}. */
    private static void wrapByCharacters(String line, LineMeasurer measurer,
                                         float contentWidth, List<String> out,
                                         StringBuilder current) {
        int start = 0;
        while (start < line.length()) {
            if (Thread.currentThread().isInterrupted()) throw new java.util.concurrent.CancellationException("已取消排版");
            final String prefix = current.toString();
            int low = start, high = nextBoundary(line, start, Math.min(line.length(), start + 32));
            while (measurer.measureWidth(prefix + line.substring(start, high)) <= contentWidth) {
                low = high;
                if (high == line.length()) break;
                high = nextBoundary(line, start, Math.min(line.length(), start + (high - start) * 2));
            }
            while (low < high) {
                int mid = low + (high - low + 1) / 2;
                if (mid < line.length() && Character.isLowSurrogate(line.charAt(mid))
                        && mid > start && Character.isHighSurrogate(line.charAt(mid - 1))) mid--;
                if (mid <= low) break;
                if (measurer.measureWidth(prefix + line.substring(start, mid)) <= contentWidth) low = mid;
                else high = mid - 1;
            }
            int end = low;
            if (end == start) {
                if (current.length() > 0) { out.add(current.toString()); current.setLength(0); continue; }
                end = start + Character.charCount(line.codePointAt(start));
            }
            // Keep combining marks and variation selectors with the preceding character.
            while (end < line.length()) {
                int cp = line.codePointAt(end), type = Character.getType(cp);
                if (type != Character.NON_SPACING_MARK && type != Character.COMBINING_SPACING_MARK
                        && cp != 0xFE0F && cp != 0xFE0E) break;
                end += Character.charCount(cp);
            }
            current.append(line, start, end);
            start = end;
            if (start < line.length()) { out.add(current.toString()); current.setLength(0); }
        }
    }

    private static int nextBoundary(String line, int start, int end) {
        if (end < line.length() && end > start && Character.isLowSurrogate(line.charAt(end))
                && Character.isHighSurrogate(line.charAt(end - 1))) end--;
        return Math.max(start + Character.charCount(line.codePointAt(start)), end);
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/VideoExporter.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.graphics.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.util.*;

/** Sequential decode, bounded frame memory, lossless disk cache only for reversed slices. */
final class VideoExporter {
    private VideoExporter(){ }
    static void export(Context context,List<AudioPipeline.Segment> segments,AnimationEdits edits,
                       File output,int width,int height,int requestedFps,int frameLimit,int loops,
                       int bitrate,String mime,String label,AudioPipeline.Check check,
                       AudioPipeline.Progress progress)throws Exception {
        double passDuration=0;
        for(AudioPipeline.Segment s:segments)passDuration+=(s.endUs-s.startUs)/1e6/s.speed;
        if(passDuration<=0)throw new IOException("没有保留的片段");
        double duration=passDuration*loops;
        if(duration>frameLimit)throw new IOException("帧数上限不足以覆盖视频；请提高上限至至少 "+(long)Math.ceil(duration)+" 帧，或缩短片段");
        double fps=Math.min(requestedFps,frameLimit/duration);
        int total=Math.max(1,(int)Math.floor(duration*fps));
        if(total<segments.size()*loops)throw new IOException("片段数超过帧预算，请提高帧数上限");
        Runtime r=Runtime.getRuntime();long available=r.maxMemory()-(r.totalMemory()-r.freeMemory());
        long safePixels=Math.max(65536,Math.min(r.maxMemory()/32,Math.max(65536,available/32)));
        if((long)width*height>safePixels){double scale=Math.sqrt(safePixels/((double)width*height));width=(int)(width*scale);height=(int)(height*scale);}
        try(Mp4Encoder encoder=new Mp4Encoder(output,width,height,Math.max(1,(int)Math.round(fps)),bitrate,mime,label)) {
            Bitmap frame=Bitmap.createBitmap(encoder.width,encoder.height,Bitmap.Config.ARGB_8888);
            Canvas canvas=new Canvas(frame);Paint paint=FrameEditor.createPaint(edits);
            int[] emitted={0};double[] elapsed={0};
            progress.update(0,"实际导出："+encoder.width+"×"+encoder.height+" · "+String.format(Locale.ROOT,"%.2f FPS · %.2f Mbps",fps,encoder.bitrate/1e6));
            try {
                for(int pass=0;pass<loops;pass++)for(int i=0;i<segments.size();i++) {
                    check.check();AudioPipeline.Segment s=segments.get(i);
                    double segmentDuration=(s.endUs-s.startUs)/1e6/s.speed;
                    int end=Math.min(total,Math.max(emitted[0]+1,(int)Math.round((elapsed[0]+segmentDuration)*fps)));
                    int count=end-emitted[0];elapsed[0]+=segmentDuration;
                    if(count<=0)continue;
                    VideoFrameDecoder.Info info=VideoFrameDecoder.probe(context,s.uri);
                    int[] bounds=FrameEditor.decodeBounds(info.orientedWidth(),info.orientedHeight(),encoder.width,encoder.height,edits);
                    final int startFrame=emitted[0];final int[] produced={0};final boolean[] seen={false};
                    File backing=File.createTempFile("video_frames_",".cache",context.getCacheDir());
                    try(IndexedFrameStore store=s.reverse?new IndexedFrameStore(backing,encoder.width*encoder.height*4,()->Thread.currentThread().isInterrupted()):null) {
                        byte[] raw=s.reverse?new byte[encoder.width*encoder.height*4]:null;
                        if(s.reverse&&context.getCacheDir().getUsableSpace()<(long)raw.length*count+32L*1024*1024)throw new IOException("倒放缓存空间不足，请降低分辨率或缩短片段");
                        ByteBuffer pixels=s.reverse?ByteBuffer.wrap(raw):null;
                        VideoFrameDecoder.decode(context,s.uri,s.startUs,s.endUs,Math.max(0.2,fps/s.speed),count,bounds[0],bounds[1],
                            ()->Thread.currentThread().isInterrupted(),(bitmap,index,expected,pts)-> {
                                check.check();
                                try{FrameEditor.drawBitmap(canvas,bitmap,0xff000000,edits,paint);}finally{bitmap.recycle();}
                                seen[0]=true;
                                int desired=(int)Math.min(count,1+(long)Math.floor(Math.max(0,pts-s.startUs)/1e6/s.speed*fps));
                                if(s.reverse){pixels.clear();frame.copyPixelsToBuffer(pixels);}
                                while(produced[0]<desired){check.check();if(s.reverse)store.add(raw);else encoder.encodeFrame(frame,Math.round((startFrame+produced[0])*1e6/fps));produced[0]++;}
                                progress.update((int)(900L*(startFrame+produced[0])/total),"正在剪辑视频："+(startFrame+produced[0])+" / "+total+" 帧");
                            });
                        if(!seen[0])throw new IOException("视频片段无法解码，请换用本机支持的编码格式");
                        while(produced[0]<count){check.check();if(s.reverse)store.add(raw);else encoder.encodeFrame(frame,Math.round((startFrame+produced[0])*1e6/fps));produced[0]++;}
                        if(s.reverse)for(int n=0;n<count;n++){check.check();store.read(count-1-n,raw);pixels.clear();frame.copyPixelsFromBuffer(pixels);encoder.encodeFrame(frame,Math.round((startFrame+n)*1e6/fps));}
                    }finally{backing.delete();}
                    emitted[0]+=count;
                }
                encoder.finish();
            }finally{frame.recycle();}
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/VideoFrameDecoder.java': r'''package com.qi.formatconverter;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.graphics.ImageFormat;
import android.graphics.Matrix;
import android.graphics.Rect;
import android.media.Image;
import android.media.MediaCodec;
import android.media.MediaCodecInfo;
import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.net.Uri;

import java.io.IOException;
import java.nio.ByteBuffer;

/**
 * Sequential video decoder used by video->GIF.
 *
 * MediaMetadataRetriever is excellent for thumbnails and one-off random seeks, but repeatedly
 * seeking hundreds of frames can be extremely slow on some vendor decoders and cannot be
 * interrupted promptly. This class walks the compressed stream once with MediaExtractor +
 * MediaCodec, so the first frame arrives quickly and cancellation is checked every few ms.
 */
final class VideoFrameDecoder {
    private static final long CODEC_STALL_TIMEOUT_NS = 15_000_000_000L;

    interface CancelCheck {
        boolean isCancelled();
    }

    interface FrameConsumer {
        void onFrame(Bitmap bitmap, int emittedIndex, int expectedCount, long presentationTimeUs)
                throws Exception;
    }

    static final class Info {
        final long durationUs;
        final int width;
        final int height;
        final int rotation;
        final String mime;
        final int bitrate;
        final int frameRate;

        Info(
                long durationUs, int width, int height, int rotation, String mime,
                int bitrate, int frameRate) {
            this.durationUs = durationUs;
            this.width = width;
            this.height = height;
            this.rotation = rotation;
            this.mime = mime;
            this.bitrate = Math.max(0, bitrate);
            this.frameRate = Math.max(0, frameRate);
        }

        int orientedWidth() {
            return rotation == 90 || rotation == 270 ? height : width;
        }

        int orientedHeight() {
            return rotation == 90 || rotation == 270 ? width : height;
        }
    }

    static Info probe(Context context, Uri uri) throws IOException {
        try (AssetFileDescriptor afd = context.getContentResolver().openAssetFileDescriptor(uri, "r")) {
            if (afd == null) throw new IOException("无法打开视频文件");
            MediaExtractor extractor = new MediaExtractor();
            try {
                setDataSource(extractor, afd);
                int track = findVideoTrack(extractor);
                if (track < 0) throw new IOException("文件中没有可解码的视频轨道");
                MediaFormat format = extractor.getTrackFormat(track);
                String mime = format.getString(MediaFormat.KEY_MIME);
                long durationUs = getLong(format, MediaFormat.KEY_DURATION, 0L);
                int width = getInt(format, MediaFormat.KEY_WIDTH, 0);
                int height = getInt(format, MediaFormat.KEY_HEIGHT, 0);
                int rotation = getInt(format, MediaFormat.KEY_ROTATION, 0);
                int bitrate = getInt(format, MediaFormat.KEY_BIT_RATE, 0);
                int frameRate = getInt(format, MediaFormat.KEY_FRAME_RATE, 0);
                return new Info(durationUs, Math.max(1, width), Math.max(1, height),
                        normalizeRotation(rotation), mime == null ? "video/*" : mime,
                        bitrate, frameRate);
            } finally {
                extractor.release();
            }
        }
    }

    static int decode(
            Context context,
            Uri uri,
            long startUs,
            long endUs,
            double fps,
            int maxFrames,
            int outputWidth,
            int outputHeight,
            CancelCheck cancelCheck,
            FrameConsumer consumer) throws Exception {
        if (fps <= 0) throw new IllegalArgumentException("帧率必须大于 0");
        if (maxFrames <= 0) return 0;

        try (AssetFileDescriptor afd = context.getContentResolver().openAssetFileDescriptor(uri, "r")) {
            if (afd == null) throw new IOException("无法打开视频文件");
            MediaExtractor extractor = new MediaExtractor();
            MediaCodec codec = null;
            try {
                setDataSource(extractor, afd);
                int track = findVideoTrack(extractor);
                if (track < 0) throw new IOException("文件中没有可解码的视频轨道");
                extractor.selectTrack(track);
                MediaFormat inputFormat = extractor.getTrackFormat(track);
                String mime = inputFormat.getString(MediaFormat.KEY_MIME);
                if (mime == null) throw new IOException("无法识别视频编码");

                long durationUs = getLong(inputFormat, MediaFormat.KEY_DURATION, 0L);
                long safeStartUs = Math.max(0L, startUs);
                long safeEndUs = endUs <= 0 ? durationUs : Math.min(durationUs, endUs);
                if (safeEndUs <= safeStartUs) throw new IOException("截取时间范围无效");

                long intervalUs = Math.max(1L, Math.round(1_000_000.0 / fps));
                int expectedCount = Math.min(maxFrames,
                        Math.max(1, (int) Math.ceil((safeEndUs - safeStartUs) / (double) intervalUs)));
                long nextTargetUs = safeStartUs;

                // Start at the previous key frame, then discard decoded frames until startUs.
                extractor.seekTo(safeStartUs, MediaExtractor.SEEK_TO_PREVIOUS_SYNC);

                // Reuse all original codec-specific keys and request a CPU-readable flexible YUV
                // output. Some vendor codecs require the original CSD buffers to be untouched.
                MediaFormat decodeFormat = inputFormat;
                try {
                    decodeFormat.setInteger(MediaFormat.KEY_COLOR_FORMAT,
                            MediaCodecInfo.CodecCapabilities.COLOR_FormatYUV420Flexible);
                } catch (Exception ignored) { }

                codec = MediaCodec.createDecoderByType(mime);
                codec.configure(decodeFormat, null, null, 0);
                codec.start();

                boolean inputEos = false;
                boolean outputEos = false;
                int emitted = 0;
                int rotation = normalizeRotation(
                        getInt(inputFormat, MediaFormat.KEY_ROTATION, 0));
                int decodeMaxWidth = rotation == 90 || rotation == 270
                        ? outputHeight : outputWidth;
                int decodeMaxHeight = rotation == 90 || rotation == 270
                        ? outputWidth : outputHeight;
                MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
                // Reused across frames; Bitmap.createBitmap copies the pixels before the next
                // decode, so one large ARGB allocation is enough for the whole video segment.
                int[][] argbScratch = new int[1][];
                long lastCodecProgressNs = System.nanoTime();

                while (!outputEos && emitted < expectedCount) {
                    checkCancelled(cancelCheck);

                    if (!inputEos) {
                        int inputIndex = codec.dequeueInputBuffer(8_000);
                        if (inputIndex >= 0) {
                            ByteBuffer input = codec.getInputBuffer(inputIndex);
                            if (input == null) {
                                codec.queueInputBuffer(inputIndex, 0, 0, 0,
                                        MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                                inputEos = true;
                                lastCodecProgressNs = System.nanoTime();
                            } else {
                                input.clear();
                                long sampleTimeUs = extractor.getSampleTime();
                                if (sampleTimeUs < 0 || sampleTimeUs >= safeEndUs) {
                                    codec.queueInputBuffer(inputIndex, 0, 0,
                                            Math.max(0L, safeEndUs),
                                            MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                                    inputEos = true;
                                    lastCodecProgressNs = System.nanoTime();
                                } else {
                                    int sampleSize = extractor.readSampleData(input, 0);
                                    if (sampleSize < 0) {
                                        codec.queueInputBuffer(inputIndex, 0, 0,
                                                Math.max(0L, sampleTimeUs),
                                                MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                                        inputEos = true;
                                        lastCodecProgressNs = System.nanoTime();
                                    } else {
                                        codec.queueInputBuffer(inputIndex, 0, sampleSize,
                                                sampleTimeUs, 0);
                                        extractor.advance();
                                        lastCodecProgressNs = System.nanoTime();
                                    }
                                }
                            }
                        }
                    }

                    int outputIndex = codec.dequeueOutputBuffer(info, 8_000);
                    if (outputIndex == MediaCodec.INFO_TRY_AGAIN_LATER) {
                        if (System.nanoTime() - lastCodecProgressNs
                                > CODEC_STALL_TIMEOUT_NS) {
                            throw new IOException("系统视频解码器超过 15 秒没有进展");
                        }
                        continue;
                    }
                    if (outputIndex == MediaCodec.INFO_OUTPUT_FORMAT_CHANGED) {
                        lastCodecProgressNs = System.nanoTime();
                        continue;
                    }
                    if (outputIndex < 0) continue;
                    lastCodecProgressNs = System.nanoTime();

                    try {
                        long ptsUs = info.presentationTimeUs;
                        boolean eos = (info.flags & MediaCodec.BUFFER_FLAG_END_OF_STREAM) != 0;
                        if ((info.flags & MediaCodec.BUFFER_FLAG_CODEC_CONFIG) == 0
                                && ptsUs >= safeStartUs && ptsUs < safeEndUs
                                && ptsUs + intervalUs / 3 >= nextTargetUs
                                && emitted < expectedCount) {
                            checkCancelled(cancelCheck);
                            Image image = codec.getOutputImage(outputIndex);
                            if (image != null) {
                                Bitmap bitmap = null;
                                try {
                                    bitmap = imageToBitmap(
                                            image, decodeMaxWidth, decodeMaxHeight,
                                            cancelCheck, argbScratch);
                                } finally {
                                    image.close();
                                }
                                bitmap = rotateReplacing(bitmap, rotation);
                                try {
                                    consumer.onFrame(bitmap, emitted, expectedCount, ptsUs);
                                } catch (Exception error) {
                                    if (bitmap != null && !bitmap.isRecycled()) bitmap.recycle();
                                    throw error;
                                }
                                emitted++;
                                do {
                                    nextTargetUs += intervalUs;
                                } while (nextTargetUs <= ptsUs);
                            }
                        }
                        outputEos = eos || ptsUs >= safeEndUs;
                    } finally {
                        codec.releaseOutputBuffer(outputIndex, false);
                    }
                }
                return emitted;
            } finally {
                if (codec != null) {
                    try { codec.stop(); } catch (Exception ignored) { }
                    try { codec.release(); } catch (Exception ignored) { }
                }
                extractor.release();
            }
        }
    }

    private static void setDataSource(MediaExtractor extractor, AssetFileDescriptor afd)
            throws IOException {
        long length = afd.getLength();
        if (length >= 0) {
            extractor.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), length);
        } else {
            extractor.setDataSource(afd.getFileDescriptor());
        }
    }

    private static int findVideoTrack(MediaExtractor extractor) {
        for (int i = 0; i < extractor.getTrackCount(); i++) {
            MediaFormat format = extractor.getTrackFormat(i);
            String mime = format.getString(MediaFormat.KEY_MIME);
            if (mime != null && mime.startsWith("video/")) return i;
        }
        return -1;
    }

    private static Bitmap imageToBitmap(
            Image image, int maxOutputWidth, int maxOutputHeight,
            CancelCheck cancelCheck, int[][] argbScratch)
            throws IOException, InterruptedException {
        if (image.getFormat() != ImageFormat.YUV_420_888) {
            throw new IOException("系统解码器返回了不支持的像素格式：" + image.getFormat());
        }
        Rect crop = image.getCropRect();
        int sourceWidth = crop.width();
        int sourceHeight = crop.height();
        double scale = Math.min(
                Math.max(1, maxOutputWidth) / (double) sourceWidth,
                Math.max(1, maxOutputHeight) / (double) sourceHeight);
        scale = Math.min(1.0, scale);
        int width = Math.max(1, (int) Math.round(sourceWidth * scale));
        int height = Math.max(1, (int) Math.round(sourceHeight * scale));
        Image.Plane[] planes = image.getPlanes();
        if (planes.length < 3) throw new IOException("视频帧像素平面不完整");

        ByteBuffer yBuffer = planes[0].getBuffer().duplicate();
        ByteBuffer uBuffer = planes[1].getBuffer().duplicate();
        ByteBuffer vBuffer = planes[2].getBuffer().duplicate();
        int yBase = yBuffer.position();
        int uBase = uBuffer.position();
        int vBase = vBuffer.position();
        int yRowStride = planes[0].getRowStride();
        int yPixelStride = planes[0].getPixelStride();
        int uRowStride = planes[1].getRowStride();
        int uPixelStride = planes[1].getPixelStride();
        int vRowStride = planes[2].getRowStride();
        int vPixelStride = planes[2].getPixelStride();

        int maxYIndex = yBase + (crop.bottom - 1) * yRowStride
                + (crop.right - 1) * yPixelStride;
        int maxUvRow = (crop.bottom - 1) >> 1;
        int maxUvColumn = (crop.right - 1) >> 1;
        int maxUIndex = uBase + maxUvRow * uRowStride + maxUvColumn * uPixelStride;
        int maxVIndex = vBase + maxUvRow * vRowStride + maxUvColumn * vPixelStride;
        if (maxYIndex < 0 || maxYIndex >= yBuffer.limit()
                || maxUIndex < 0 || maxUIndex >= uBuffer.limit()
                || maxVIndex < 0 || maxVIndex >= vBuffer.limit()) {
            throw new IOException("视频帧像素平面尺寸不正确");
        }

        int pixelCount = width * height;
        int[] argb = argbScratch[0];
        if (argb == null || argb.length < pixelCount) {
            argb = new int[pixelCount];
            argbScratch[0] = argb;
        }
        int out = 0;
        for (int row = 0; row < height; row++) {
            if ((row & 7) == 0) checkCancelled(cancelCheck);
            int srcY = crop.top + Math.min(sourceHeight - 1,
                    (int) (((long) row * sourceHeight + height / 2L) / height));
            int uvY = srcY >> 1;
            int yRowOffset = yBase + srcY * yRowStride;
            int uvRowOffsetU = uBase + uvY * uRowStride;
            int uvRowOffsetV = vBase + uvY * vRowStride;
            int previousUvX = -1;
            int u = 0;
            int v = 0;
            for (int col = 0; col < width; col++) {
                int srcX = crop.left + Math.min(sourceWidth - 1,
                        (int) (((long) col * sourceWidth + width / 2L) / width));
                int uvX = srcX >> 1;
                if (uvX != previousUvX) {
                    u = (uBuffer.get(uvRowOffsetU + uvX * uPixelStride) & 0xFF) - 128;
                    v = (vBuffer.get(uvRowOffsetV + uvX * vPixelStride) & 0xFF) - 128;
                    previousUvX = uvX;
                }
                int y = yBuffer.get(yRowOffset + srcX * yPixelStride) & 0xFF;

                int c = Math.max(0, y - 16);
                int r = (298 * c + 409 * v + 128) >> 8;
                int g = (298 * c - 100 * u - 208 * v + 128) >> 8;
                int b = (298 * c + 516 * u + 128) >> 8;
                argb[out++] = 0xFF000000
                        | (clamp8(r) << 16)
                        | (clamp8(g) << 8)
                        | clamp8(b);
            }
        }
        checkCancelled(cancelCheck);
        Bitmap bitmap = Bitmap.createBitmap(argb, width, height, Bitmap.Config.ARGB_8888);
        // Every converted YUV pixel is opaque. Marking that fact avoids an otherwise unnecessary
        // full-frame canvas copy in the common single-video / matching-aspect-ratio path.
        bitmap.setHasAlpha(false);
        return bitmap;
    }

    private static int clamp8(int value) {
        return value < 0 ? 0 : Math.min(255, value);
    }

    private static Bitmap rotateReplacing(Bitmap source, int degrees) {
        int normalized = normalizeRotation(degrees);
        if (normalized == 0) return source;
        Matrix matrix = new Matrix();
        matrix.postRotate(normalized);
        Bitmap rotated = Bitmap.createBitmap(source, 0, 0,
                source.getWidth(), source.getHeight(), matrix, true);
        rotated.setHasAlpha(false);
        if (rotated != source) source.recycle();
        return rotated;
    }

    private static int normalizeRotation(int rotation) {
        int value = ((rotation % 360) + 360) % 360;
        if (value == 90 || value == 180 || value == 270) return value;
        return 0;
    }

    private static int getInt(MediaFormat format, String key, int fallback) {
        try {
            return format.containsKey(key) ? format.getInteger(key) : fallback;
        } catch (Exception ignored) {
            return fallback;
        }
    }

    private static long getLong(MediaFormat format, String key, long fallback) {
        try {
            return format.containsKey(key) ? format.getLong(key) : fallback;
        } catch (Exception ignored) {
            return fallback;
        }
    }

    private static void checkCancelled(CancelCheck cancelCheck) throws InterruptedException {
        if (Thread.currentThread().isInterrupted()
                || (cancelCheck != null && cancelCheck.isCancelled())) {
            throw new InterruptedException("cancelled");
        }
    }

    private VideoFrameDecoder() { }
}
''',
    'app/src/main/java/com/qi/formatconverter/XmlKit.java': r'''package com.qi.formatconverter;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Pure-Java XML parser and writer with zero third-party dependencies.
 *
 * <p>The parser accepts well-formed XML documents: the declaration, processing
 * instructions, comments, DOCTYPE declarations (internal subsets are skipped),
 * CDATA sections, the five predefined entities plus numeric character references.
 * Namespace prefixes are kept verbatim inside element names (no resolution).
 *
 * <p>Conversions between XML and the JSON object tree follow the widely used
 * org.json conventions:
 * <ul>
 *   <li>attributes become keys prefixed with "@"</li>
 *   <li>mixed text content becomes the "#text" key</li>
 *   <li>repeated sibling elements become a JSON array</li>
 *   <li>a leaf element with only text becomes an inferred scalar
 *       (boolean / null / number / string)</li>
 *   <li>an empty element becomes ""</li>
 * </ul>
 *
 * <p>All error messages are in Chinese and include the offending line number.
 */
final class XmlKit {

    private XmlKit() { }

    private static final int MAX_DEPTH = 256;

    /** One XML element: name, ordered attributes and ordered content nodes. */
    static final class XmlNode {
        final String name;
        final LinkedHashMap<String, String> attributes = new LinkedHashMap<>();
        final List<Object> content = new ArrayList<>(); // String or XmlNode

        XmlNode(String name) {
            if (name == null || name.isEmpty()) {
                throw new IllegalArgumentException("XML 元素名为空");
            }
            this.name = name;
        }

        boolean hasElementChildren() {
            for (Object item : content) {
                if (item instanceof XmlNode) return true;
            }
            return false;
        }

        String textContent() {
            StringBuilder sb = new StringBuilder();
            for (Object item : content) {
                if (item instanceof String) sb.append((String) item);
            }
            return sb.toString();
        }
    }

    /** Parses a document and returns its root element. */
    public static XmlNode parseDocument(String xml) {
        if (xml == null) throw new IllegalArgumentException("XML 内容为空");
        String s = xml;
        if (!s.isEmpty() && s.charAt(0) == '\uFEFF') s = s.substring(1);
        XmlParser parser = new XmlParser(s);
        return parser.parseDocument();
    }

    // ---------------------------------------------------------------------
    // XML -> JSON tree
    // ---------------------------------------------------------------------

    /** Converts the document (root element) into a JSON-ready object tree. */
    public static Object toJsonValue(XmlNode root) {
        return elementToValue(root);
    }

    private static Object elementToValue(XmlNode element) {
        if (!element.hasElementChildren() && element.attributes.isEmpty()) {
            // Leaf element: infer the scalar type from its text (trimmed for readability).
            return inferScalar(element.textContent().trim());
        }
        Map<String, Object> map = new LinkedHashMap<>();
        for (Map.Entry<String, String> attribute : element.attributes.entrySet()) {
            map.put("@" + attribute.getKey(), attribute.getValue());
        }
        Map<String, Object> children = new LinkedHashMap<>();
        for (Object item : element.content) {
            if (item instanceof XmlNode) {
                XmlNode child = (XmlNode) item;
                Object value = elementToValue(child);
                Object existing = children.get(child.name);
                if (existing == null) {
                    children.put(child.name, value);
                } else if (existing instanceof List) {
                    @SuppressWarnings("unchecked")
                    List<Object> list = (List<Object>) existing;
                    list.add(value);
                } else {
                    List<Object> list = new ArrayList<>();
                    list.add(existing);
                    list.add(value);
                    children.put(child.name, list);
                }
            }
        }
        map.putAll(children);
        String text = element.textContent();
        if (!text.trim().isEmpty()) {
            map.put("#text", inferScalar(text.trim()));
        }
        return map;
    }

    /** org.json-style inference so numbers and booleans survive XML -> JSON. */
    static Object inferScalar(String text) {
        if (text == null) return "";
        String t = text.trim();
        if (t.equals("true")) return Boolean.TRUE;
        if (t.equals("false")) return Boolean.FALSE;
        if (t.equals("null")) return null;
        if (t.matches("-?\\d+")) {
            try {
                return Long.parseLong(t);
            } catch (NumberFormatException tooBig) {
                return text;
            }
        }
        if (t.matches("[-+]?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?")
                || t.matches("[-+]?\\d+[eE][-+]?\\d+")) {
            return Double.parseDouble(t);
        }
        return text;
    }

    // ---------------------------------------------------------------------
    // XML -> plain text
    // ---------------------------------------------------------------------

    /** Extracts readable text: leaf texts in document order, one per line. */
    public static String toPlainText(XmlNode root) {
        StringBuilder sb = new StringBuilder();
        collectText(root, sb);
        return sb.toString().trim();
    }

    private static void collectText(XmlNode element, StringBuilder sb) {
        for (Object item : element.content) {
            if (item instanceof String) {
                String text = ((String) item).trim();
                if (!text.isEmpty()) {
                    sb.append(collapseSpaces(text)).append('\n');
                }
            } else {
                collectText((XmlNode) item, sb);
            }
        }
    }

    private static String collapseSpaces(String s) {
        return s.replaceAll("\\s+", " ");
    }

    // ---------------------------------------------------------------------
    // JSON tree -> XML
    // ---------------------------------------------------------------------

    /** Serializes an object tree as a complete XML document with the given root name. */
    public static String write(Object value, String rootName) {
        String root = sanitizeName(rootName == null || rootName.trim().isEmpty()
                ? "root" : rootName.trim());
        StringBuilder sb = new StringBuilder();
        sb.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        writeElement(root, value, sb, 0);
        return sb.toString();
    }

    private static void writeElement(String name, Object value, StringBuilder sb, int indent) {
        if (value instanceof Map) {
            writeElementWithChildren(name, (Map<?, ?>) value, sb, indent);
        } else if (value instanceof List) {
            sb.append(indentSpaces(indent)).append('<').append(name).append(">\n");
            for (Object item : (List<?>) value) {
                writeElement("item", item, sb, indent + 2);
            }
            sb.append(indentSpaces(indent)).append("</").append(name).append(">\n");
        } else {
            writeTextElement(name, scalarText(value), sb, indent);
        }
    }

    private static void writeElementWithChildren(String name, Map<?, ?> map, StringBuilder sb,
                                                  int indent) {
        List<Object> children = new ArrayList<>();
        List<Object> attributes = new ArrayList<>();
        String text = null;
        for (Map.Entry<?, ?> entry : map.entrySet()) {
            String key = String.valueOf(entry.getKey());
            if (key.startsWith("@")) {
                attributes.add(new String[]{sanitizeName(key.substring(1)),
                        scalarText(entry.getValue())});
            } else if (key.equals("#text")) {
                text = scalarText(entry.getValue());
            } else {
                children.add(new Object[]{key, entry.getValue()});
            }
        }
        if (children.isEmpty() && attributes.isEmpty() && text == null) {
            sb.append(indentSpaces(indent)).append('<').append(name).append("/>\n");
            return;
        }
        if (children.isEmpty()) {
            // Attributes and/or text only: single line element.
            sb.append(indentSpaces(indent)).append('<').append(name);
            appendAttributes(attributes, sb);
            if (text == null) {
                sb.append("/>\n");
            } else {
                sb.append('>').append(escapeText(text)).append("</").append(name).append(">\n");
            }
            return;
        }
        sb.append(indentSpaces(indent)).append('<').append(name);
        appendAttributes(attributes, sb);
        sb.append(">\n");
        if (text != null && !text.isEmpty()) {
            sb.append(indentSpaces(indent + 2)).append(escapeText(text)).append('\n');
        }
        for (Object child : children) {
            Object[] pair = (Object[]) child;
            String childName = sanitizeName(String.valueOf(pair[0]));
            Object value = pair[1];
            if (value instanceof List) {
                // An array under a key becomes repeated same-name elements so that
                // the XML -> JSON direction rebuilds the array (org.json convention).
                List<?> items = (List<?>) value;
                if (items.isEmpty()) {
                    // Keep the key present even for an empty array.
                    sb.append(indentSpaces(indent + 2)).append('<').append(childName)
                            .append("/>\n");
                } else {
                    for (Object item : items) {
                        writeElement(childName, item, sb, indent + 2);
                    }
                }
            } else {
                writeElement(childName, value, sb, indent + 2);
            }
        }
        sb.append(indentSpaces(indent)).append("</").append(name).append(">\n");
    }

    private static void appendAttributes(List<Object> attributes, StringBuilder sb) {
        for (Object attribute : attributes) {
            String[] pair = (String[]) attribute;
            sb.append(' ').append(pair[0]).append("=\"")
                    .append(escapeAttribute(pair[1])).append('"');
        }
    }

    private static void writeTextElement(String name, String text, StringBuilder sb, int indent) {
        if (text == null || text.isEmpty()) {
            sb.append(indentSpaces(indent)).append('<').append(name).append("/>\n");
            return;
        }
        if (text.contains("\n")) {
            // Lines are written raw (no indentation) so the exact text content
            // survives the XML -> JSON round trip.
            sb.append(indentSpaces(indent)).append('<').append(name).append(">\n");
            for (String line : text.split("\n", -1)) {
                sb.append(escapeText(line)).append('\n');
            }
            sb.append(indentSpaces(indent)).append("</").append(name).append(">\n");
        } else {
            sb.append(indentSpaces(indent)).append('<').append(name).append('>')
                    .append(escapeText(text)).append("</").append(name).append(">\n");
        }
    }

    private static String scalarText(Object value) {
        if (value == null) return "";
        if (value instanceof Double) {
            double d = (Double) value;
            if (Double.isNaN(d) || Double.isInfinite(d)) return value.toString();
            if (d == Math.rint(d) && Math.abs(d) < 1e15) {
                return Long.toString((long) d);
            }
            return Double.toString(d);
        }
        if (value instanceof Number || value instanceof Boolean) return value.toString();
        return String.valueOf(value);
    }

    static String escapeText(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }

    static String escapeAttribute(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;");
    }

    static String sanitizeName(String raw) {
        String name = raw.trim();
        if (name.isEmpty()) return "_";
        if (name.startsWith("@")) name = name.substring(1);
        StringBuilder sb = new StringBuilder(name.length() + 2);
        int i = 0;
        boolean first = true;
        while (i < name.length()) {
            int cp = name.codePointAt(i);
            i += Character.charCount(cp);
            boolean valid = first ? isNameStartChar(cp) : isNameChar(cp);
            if (!valid && first) {
                sb.append('_').appendCodePoint(cp);
                first = false;
            } else if (!valid) {
                sb.append('_');
            } else {
                sb.appendCodePoint(cp);
                first = false;
            }
        }
        return sb.length() == 0 ? "_" : sb.toString();
    }

    /** XML names allow Unicode letters (including CJK ideographs). */
    static boolean isNameStartChar(int cp) {
        return cp == '_' || cp == ':' || (cp >= 'a' && cp <= 'z')
                || (cp >= 'A' && cp <= 'Z') || Character.isLetter(cp);
    }

    static boolean isNameChar(int cp) {
        return isNameStartChar(cp) || (cp >= '0' && cp <= '9')
                || cp == '-' || cp == '.' || Character.isLetter(cp);
    }

    private static String indentSpaces(int indent) {
        if (indent <= 0) return "";
        StringBuilder sb = new StringBuilder(indent);
        for (int i = 0; i < indent; i++) sb.append(' ');
        return sb.toString();
    }

    // ---------------------------------------------------------------------
    // Parser
    // ---------------------------------------------------------------------

    private static final class XmlParser {
        private final String s;
        private int pos = 0;
        private int depth = 0;

        XmlParser(String s) {
            this.s = s;
        }

        private IllegalArgumentException err(String message) {
            int line = 1 + countChar(s, 0, Math.min(pos, s.length()), '\n');
            return new IllegalArgumentException("XML 第 " + line + " 行：" + message);
        }

        private static int countChar(String s, int from, int to, char c) {
            int count = 0;
            for (int i = from; i < to; i++) {
                if (s.charAt(i) == c) count++;
            }
            return count;
        }

        XmlNode parseDocument() {
            skipWhitespace();
            skipProlog();
            skipWhitespace();
            if (atEnd()) throw err("XML 内容为空");
            if (peek() != '<') throw err("XML 必须以 '<' 开始");
            XmlNode root = parseElement();
            skipWhitespace();
            skipPrologTrailing();
            if (!atEnd()) throw err("XML 文档在根元素之后还有多余内容");
            return root;
        }

        private void skipPrologTrailing() {
            while (!atEnd()) {
                if (s.startsWith("<!--", pos)) {
                    skipUntil("-->");
                } else if (s.startsWith("<?", pos)) {
                    skipUntil("?>");
                } else {
                    return;
                }
                skipWhitespace();
            }
        }

        private void skipProlog() {
            while (!atEnd()) {
                if (s.startsWith("<?", pos)) {
                    skipUntil("?>");
                } else if (s.startsWith("<!--", pos)) {
                    skipUntil("-->");
                } else if (s.startsWith("<!", pos)) {
                    skipDoctype();
                } else {
                    return;
                }
                skipWhitespace();
            }
        }

        private void skipDoctype() {
            // <!DOCTYPE ... > with a possible [internal subset].
            int close = findDoctypeEnd();
            if (close < 0) throw err("XML DOCTYPE 声明未闭合");
            pos = close;
        }

        private int findDoctypeEnd() {
            int i = pos;
            int brackets = 0;
            while (i < s.length()) {
                char c = s.charAt(i);
                if (c == '[') brackets++;
                else if (c == ']') brackets--;
                else if (c == '>' && brackets <= 0) return i + 1;
                i++;
            }
            return -1;
        }

        private void skipUntil(String marker) {
            int found = s.indexOf(marker, pos);
            if (found < 0) throw err("XML 注释或声明未闭合");
            pos = found + marker.length();
        }

        private boolean atEnd() {
            return pos >= s.length();
        }

        private char peek() {
            if (atEnd()) throw err("XML 意外结束");
            return s.charAt(pos);
        }

        private void skipWhitespace() {
            while (!atEnd()) {
                char c = s.charAt(pos);
                if (c == ' ' || c == '\t' || c == '\n' || c == '\r') pos++;
                else break;
            }
        }

        private XmlNode parseElement() {
            if (++depth > MAX_DEPTH) throw err("XML 嵌套层级过深");
            try {
                if (peek() != '<') throw err("XML 期待 '<'");
                pos++;
                String name = readName();
                XmlNode node = new XmlNode(name);
                while (true) {
                    skipWhitespace();
                    char c = peek();
                    if (c == '>') {
                        pos++;
                        parseContent(node, name);
                        return node;
                    }
                    if (c == '/' && s.startsWith("/>", pos)) {
                        pos += 2;
                        return node;
                    }
                    String attributeName = readName();
                    skipWhitespace();
                    if (atEnd() || peek() != '=') {
                        throw err("XML 属性缺少等号（" + attributeName + "）");
                    }
                    pos++;
                    skipWhitespace();
                    String value = readAttributeValue();
                    if (node.attributes.containsKey(attributeName)) {
                        throw err("XML 属性重复（" + attributeName + "）");
                    }
                    node.attributes.put(attributeName, value);
                }
            } finally {
                depth--;
            }
        }

        private String readName() {
            int start = pos;
            if (atEnd() || !isNameStartChar(s.codePointAt(pos))) {
                throw err("XML 名称格式错误");
            }
            pos += Character.charCount(s.codePointAt(pos));
            while (!atEnd() && isNameChar(s.codePointAt(pos))) {
                pos += Character.charCount(s.codePointAt(pos));
            }
            return s.substring(start, pos);
        }

        private String readAttributeValue() {
            if (atEnd()) throw err("XML 属性值缺失");
            char quote = peek();
            if (quote != '"' && quote != '\'') {
                throw err("XML 属性值必须用引号包裹");
            }
            pos++;
            StringBuilder sb = new StringBuilder();
            while (true) {
                if (atEnd()) throw err("XML 属性值未闭合");
                char c = s.charAt(pos++);
                if (c == quote) return decodeEntities(sb.toString());
                sb.append(c);
            }
        }

        private void parseContent(XmlNode node, String name) {
            // Mixed text pieces: (String text, Boolean needsEntityDecode) — CDATA is raw.
            List<Object[]> pendingText = new ArrayList<>();
            while (true) {
                if (atEnd()) throw err("XML 元素 <" + name + "> 未闭合");
                if (s.startsWith("</", pos)) {
                    flushText(node, pendingText);
                    pos += 2;
                    String closeName = readName();
                    skipWhitespace();
                    if (atEnd() || peek() != '>') {
                        throw err("XML 结束标签格式错误（</" + closeName + ">）");
                    }
                    pos++;
                    if (!closeName.equals(name)) {
                        throw err("XML 结束标签 </" + closeName + "> 与开始标签 <" + name
                                + "> 不匹配");
                    }
                    return;
                }
                if (s.startsWith("<!--", pos)) {
                    flushText(node, pendingText);
                    skipUntil("-->");
                    continue;
                }
                if (s.startsWith("<![CDATA[", pos)) {
                    int end = s.indexOf("]]>", pos + 9);
                    if (end < 0) throw err("XML CDATA 未闭合");
                    pendingText.add(new Object[]{s.substring(pos + 9, end), Boolean.FALSE});
                    pos = end + 3;
                    continue;
                }
                if (s.startsWith("<?", pos)) {
                    flushText(node, pendingText);
                    skipUntil("?>");
                    continue;
                }
                if (peek() == '<') {
                    flushText(node, pendingText);
                    node.content.add(parseElement());
                    continue;
                }
                int start = pos;
                while (pos < s.length() && s.charAt(pos) != '<') pos++;
                pendingText.add(new Object[]{s.substring(start, pos), Boolean.TRUE});
            }
        }

        private void flushText(XmlNode node, List<Object[]> pendingText) {
            if (pendingText.isEmpty()) return;
            StringBuilder sb = new StringBuilder();
            for (Object[] piece : pendingText) {
                String text = (String) piece[0];
                boolean decode = (Boolean) piece[1];
                sb.append(decode ? decodeEntities(text) : text);
            }
            node.content.add(sb.toString());
            pendingText.clear();
        }

        private String decodeEntities(String value) {
            if (value.indexOf('&') < 0) return value;
            StringBuilder sb = new StringBuilder(value.length());
            int i = 0;
            int n = value.length();
            while (i < n) {
                char c = value.charAt(i);
                if (c != '&') {
                    sb.append(c);
                    i++;
                    continue;
                }
                int semicolon = value.indexOf(';', i + 1);
                if (semicolon < 0 || semicolon - i > 12) {
                    throw err("XML 实体格式错误（缺少分号）");
                }
                String entity = value.substring(i + 1, semicolon);
                if (entity.equals("amp")) sb.append('&');
                else if (entity.equals("lt")) sb.append('<');
                else if (entity.equals("gt")) sb.append('>');
                else if (entity.equals("quot")) sb.append('"');
                else if (entity.equals("apos")) sb.append('\'');
                else if (entity.startsWith("#x") || entity.startsWith("#X")) {
                    try {
                        sb.append((char) Integer.parseInt(entity.substring(2), 16));
                    } catch (NumberFormatException bad) {
                        throw err("XML 十六进制实体无效（&" + entity + ";）");
                    }
                } else if (entity.startsWith("#")) {
                    try {
                        sb.append((char) Integer.parseInt(entity.substring(1)));
                    } catch (NumberFormatException bad) {
                        throw err("XML 数字实体无效（&" + entity + ";）");
                    }
                } else {
                    throw err("XML 未定义的实体（&" + entity + ";）");
                }
                i = semicolon + 1;
            }
            return sb.toString();
        }
    }
}
''',
    'app/src/main/java/com/qi/formatconverter/YamlKit.java': r'''package com.qi.formatconverter;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Pure-Java YAML subset parser and writer with zero third-party dependencies.
 *
 * <p>Supported subset (covers the vast majority of real-world config/data files):
 * <ul>
 *   <li>block mappings and block sequences with indentation-based nesting</li>
 *   <li>sequences written at the same indent level as their parent key</li>
 *   <li>flow collections {@code [a, b]} and {@code {a: 1, b: 2}} (single or multi line)</li>
 *   <li>plain scalars, single/double quoted scalars (multi line folding supported)</li>
 *   <li>block scalars {@code |}, {@code >} with chomping ({@code - +}) and explicit indent</li>
 *   <li>comments, blank lines, an optional leading {@code ---} and trailing {@code ...}</li>
 *   <li>null / booleans / integers (dec, 0x, 0o) / floats (incl. .inf / .nan)</li>
 * </ul>
 *
 * <p>Explicitly unsupported (clear error messages): anchors and aliases, tags,
 * multiple documents, directives, complex keys, merge keys, tab indentation.
 *
 * <p>All error messages are in Chinese and include the offending line number.
 */
final class YamlKit {

    private YamlKit() { }

    private static final int MAX_DEPTH = 256;

    /** Parses a YAML document into Map / List / String / Long / Double / Boolean / null. */
    public static Object parse(String yaml) {
        if (yaml == null) throw new IllegalArgumentException("YAML 内容为空");
        Parser parser = new Parser(yaml);
        parser.load();
        parser.skipDocumentStart();
        if (parser.significantLines() == 0) {
            throw new IllegalArgumentException("YAML 内容为空");
        }
        Object value = parser.parseNode(0, 1);
        parser.expectDocumentEnd();
        return value;
    }

    /** Serializes a Map / List / scalar tree as block-style YAML (two-space indent). */
    public static String write(Object value) {
        StringBuilder sb = new StringBuilder();
        writeNode(value, sb, 0, true);
        return sb.toString();
    }

    // =====================================================================
    // Serializer
    // =====================================================================

    private static void writeNode(Object value, StringBuilder sb, int indent, boolean topLevel) {
        if (value instanceof Map) {
            writeMapping((Map<?, ?>) value, sb, indent, topLevel);
        } else if (value instanceof List) {
            writeSequence((List<?>) value, sb, indent, topLevel);
        } else {
            sb.append(indentSpaces(indent)).append(writeScalar(value)).append('\n');
        }
    }

    private static void writeMapping(Map<?, ?> map, StringBuilder sb, int indent, boolean topLevel) {
        if (map.isEmpty()) {
            sb.append(indentSpaces(indent)).append("{}\n");
            return;
        }
        for (Map.Entry<?, ?> entry : map.entrySet()) {
            String key = String.valueOf(entry.getKey());
            Object value = entry.getValue();
            sb.append(indentSpaces(indent)).append(writeKey(key)).append(':');
            if (value instanceof Map && !((Map<?, ?>) value).isEmpty()) {
                sb.append('\n');
                writeMapping((Map<?, ?>) value, sb, indent + 2, false);
            } else if (value instanceof List && !((List<?>) value).isEmpty()) {
                sb.append('\n');
                writeSequence((List<?>) value, sb, indent, false);
            } else if (value instanceof Map) {
                sb.append(" {}\n");
            } else if (value instanceof List) {
                sb.append(" []\n");
            } else {
                sb.append(' ').append(writeScalar(value)).append('\n');
            }
        }
    }

    private static void writeSequence(List<?> list, StringBuilder sb, int indent, boolean topLevel) {
        for (Object value : list) {
            sb.append(indentSpaces(indent)).append('-');
            if (value instanceof Map && !((Map<?, ?>) value).isEmpty()) {
                // "- key: value" inline start with following keys aligned at indent + 2.
                Map<?, ?> map = (Map<?, ?>) value;
                sb.append(' ');
                writeMappingInline(map, sb, indent + 2);
            } else if (value instanceof List && !((List<?>) value).isEmpty()) {
                sb.append(' ');
                writeSequenceInline((List<?>) value, sb, indent + 2);
            } else if (value instanceof Map) {
                sb.append(" {}\n");
            } else if (value instanceof List) {
                sb.append(" []\n");
            } else {
                sb.append(' ').append(writeScalar(value)).append('\n');
            }
        }
    }

    private static void writeMappingInline(Map<?, ?> map, StringBuilder sb, int indent) {
        boolean first = true;
        for (Map.Entry<?, ?> entry : map.entrySet()) {
            if (!first) sb.append(indentSpaces(indent));
            first = false;
            Object value = entry.getValue();
            sb.append(writeKey(String.valueOf(entry.getKey()))).append(':');
            if (value instanceof Map && !((Map<?, ?>) value).isEmpty()) {
                sb.append('\n');
                writeMapping((Map<?, ?>) value, sb, indent + 2, false);
            } else if (value instanceof List && !((List<?>) value).isEmpty()) {
                sb.append('\n');
                writeSequence((List<?>) value, sb, indent, false);
            } else if (value instanceof Map) {
                sb.append(" {}\n");
            } else if (value instanceof List) {
                sb.append(" []\n");
            } else {
                sb.append(' ').append(writeScalar(value)).append('\n');
            }
        }
    }

    private static void writeSequenceInline(List<?> list, StringBuilder sb, int indent) {
        boolean first = true;
        for (Object value : list) {
            if (!first) sb.append(indentSpaces(indent));
            first = false;
            sb.append('-');
            if (value instanceof Map && !((Map<?, ?>) value).isEmpty()) {
                sb.append(' ');
                writeMappingInline((Map<?, ?>) value, sb, indent + 2);
            } else if (value instanceof List && !((List<?>) value).isEmpty()) {
                sb.append(' ');
                writeSequenceInline((List<?>) value, sb, indent + 2);
            } else if (value instanceof Map) {
                sb.append(" {}\n");
            } else if (value instanceof List) {
                sb.append(" []\n");
            } else {
                sb.append(' ').append(writeScalar(value)).append('\n');
            }
        }
    }

    private static String indentSpaces(int indent) {
        if (indent <= 0) return "";
        StringBuilder sb = new StringBuilder(indent);
        for (int i = 0; i < indent; i++) sb.append(' ');
        return sb.toString();
    }

    private static String writeKey(String key) {
        return writeScalar((Object) key);
    }

    /** Renders a scalar; chooses plain / single-quoted / double-quoted as needed. */
    static String writeScalar(Object value) {
        if (value == null) return "null";
        if (value instanceof Boolean) return value.toString();
        if (value instanceof Double) return writeDouble((Double) value);
        if (value instanceof Number) return value.toString();
        String s = (String) value;
        if (s.isEmpty()) return "''";
        if (needsDoubleQuoted(s)) return writeDoubleQuoted(s);
        if (needsQuoting(s)) return "'" + s.replace("'", "''") + "'";
        return s;
    }

    private static String writeDouble(Double value) {
        double d = value;
        if (Double.isNaN(d)) return ".nan";
        if (d == Double.POSITIVE_INFINITY) return ".inf";
        if (d == Double.NEGATIVE_INFINITY) return "-.inf";
        if (d == Math.rint(d) && Math.abs(d) < 1e15) {
            return Long.toString((long) d);
        }
        return Double.toString(d);
    }

    private static boolean needsQuoting(String s) {
        if (scalarLooksStructured(s)) return true;
        char first = s.charAt(0);
        if (" \t".indexOf(first) >= 0 || first == '-' || first == '?'
                || first == ':' || first == ',' || first == '[' || first == ']'
                || first == '{' || first == '}' || first == '#' || first == '&'
                || first == '*' || first == '!' || first == '|' || first == '>'
                || first == '\'' || first == '"' || first == '%' || first == '@'
                || first == '`') {
            return true;
        }
        char last = s.charAt(s.length() - 1);
        if (last == ' ' || last == '\t' || last == ':') return true;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c < 0x20) return true;
            if (c == ':' && i + 1 < s.length()
                    && (s.charAt(i + 1) == ' ' || s.charAt(i + 1) == '\t')) return true;
            if (c == '#' && i > 0
                    && (s.charAt(i - 1) == ' ' || s.charAt(i - 1) == '\t')) return true;
        }
        return false;
    }

    /** True when the string would be re-read as null / bool / number instead of text. */
    private static boolean scalarLooksStructured(String s) {
        String t = s.trim();
        if (t.equals("~") || t.equalsIgnoreCase("null")) return true;
        if (t.equalsIgnoreCase("true") || t.equalsIgnoreCase("false")) return true;
        if (t.equals(".inf") || t.equals(".Inf") || t.equals(".INF")
                || t.equals("-.inf") || t.equals("-.Inf") || t.equals("-.INF")
                || t.equals("+.inf") || t.equals("+.Inf") || t.equals("+.INF")
                || t.equalsIgnoreCase(".nan")) return true;
        String cleaned = t.replace("_", "");
        if (cleaned.matches("-?\\d+")) return true;
        if (cleaned.matches("[-+]?0x[0-9a-fA-F]+")) return true;
        if (cleaned.matches("[-+]?0o[0-7]+")) return true;
        if (cleaned.matches("[-+]?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?")) return true;
        if (cleaned.matches("[-+]?\\d+[eE][-+]?\\d+")) return true;
        return false;
    }

    private static boolean needsDoubleQuoted(String s) {
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c < 0x20 || c == '\n' || c == '\r' || c == '\t') return true;
        }
        return s.indexOf('\n') >= 0 || s.indexOf('\r') >= 0;
    }

    private static String writeDoubleQuoted(String s) {
        StringBuilder sb = new StringBuilder(s.length() + 8);
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                case '\u0000': sb.append("\\0"); break;
                default:
                    if (c < 0x20) {
                        sb.append(String.format("\\x%02x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
        return sb.toString();
    }

    // =====================================================================
    // Parser
    // =====================================================================

    private static final class Parser {
        private final String[] lines;
        private final int[] indents;
        private int idx = 0;
        private int lineCount;

        Parser(String text) {
            // Normalize line endings, drop a possible BOM (TextConverter.decode strips it,
            // but keep the guard so the parser is safe when called directly).
            String s = text;
            if (!s.isEmpty() && s.charAt(0) == '\uFEFF') s = s.substring(1);
            String[] raw = s.split("\n", -1);
            List<String> collected = new ArrayList<>();
            for (String line : raw) {
                String l = line;
                if (l.endsWith("\r")) l = l.substring(0, l.length() - 1);
                collected.add(l);
            }
            // "a\n" is a single line: split("\n", -1) yields a phantom trailing empty
            // element which would otherwise inflate blank-line runs (block scalars).
            if (!collected.isEmpty() && s.endsWith("\n")
                    && collected.get(collected.size() - 1).isEmpty()) {
                collected.remove(collected.size() - 1);
            }
            lines = collected.toArray(new String[0]);
            indents = new int[lines.length];
        }

        void load() {
            int count = 0;
            for (int i = 0; i < lines.length; i++) {
                indents[i] = computeIndent(i);
                if (isSignificant(lines[i])) count++;
            }
            lineCount = count;
        }

        int significantLines() {
            return lineCount;
        }

        private int computeIndent(int i) {
            String line = lines[i];
            int indent = 0;
            while (indent < line.length() && line.charAt(indent) == ' ') indent++;
            if (indent < line.length() && line.charAt(indent) == '\t') {
                throw err(i, "YAML 不允许用 Tab 缩进，请改用空格");
            }
            return indent;
        }

        private IllegalArgumentException err(int line, String message) {
            return new IllegalArgumentException("YAML 第 " + (line + 1) + " 行：" + message);
        }

        private boolean isSignificant(String line) {
            String trimmed = line.trim();
            return !trimmed.isEmpty() && trimmed.charAt(0) != '#';
        }

        private boolean atEnd() {
            return idx >= lines.length;
        }

        private void skipInsignificant() {
            while (!atEnd() && !isSignificant(lines[idx])) idx++;
        }

        private int currentIndent() {
            skipInsignificant();
            if (atEnd()) return -1;
            return indents[idx];
        }

        /** Skips an optional single leading "---" document start marker. */
        void skipDocumentStart() {
            skipInsignificant();
            if (atEnd()) return;
            String line = lines[idx];
            if (indents[idx] == 0 && line.trim().equals("---")) {
                idx++;
            } else if (line.trim().startsWith("---")) {
                throw err(idx, "YAML 多文档（---）暂不支持，请拆分后逐个转换");
            }
        }

        /** Skips an optional single leading "---" and rejects real multi-document input. */
        void expectDocumentEnd() {
            skipInsignificant();
            if (atEnd()) return;
            String trimmed = lines[idx].trim();
            if (trimmed.equals("...")) {
                idx++;
                skipInsignificant();
                if (atEnd()) return;
            }
            if (trimmed.startsWith("---")) {
                throw err(idx, "YAML 多文档（---）暂不支持，请拆分后逐个转换");
            }
            throw err(idx, "YAML 结构错误：这里不应再出现内容");
        }

        // ------------------------------------------------------------------
        // Node parsing
        // ------------------------------------------------------------------

        Object parseNode(int minIndent, int depth) {
            if (depth > MAX_DEPTH) {
                throw err(idx, "YAML 嵌套层级过深");
            }
            skipInsignificant();
            if (atEnd()) return null;
            int indent = indents[idx];
            if (indent < minIndent) return null;
            String line = lines[idx];
            if (isSequenceEntry(line, indent)) {
                return parseSequence(indent, depth);
            }
            int colon = findMappingColon(line, indent);
            if (colon >= 0) {
                return parseMapping(indent, depth);
            }
            // Whole-line scalar document (plain / quoted / flow / block scalar).
            return parseValueAtLine(idx, indent, depth);
        }

        private boolean isSequenceEntry(String line, int indent) {
            String content = line.substring(indent);
            return content.equals("-")
                    || content.startsWith("- ")
                    || content.startsWith("-\t");
        }

        /** Finds the ':' that separates a mapping key from its value (-1 when absent). */
        private int findMappingColon(String line, int from) {
            int i = from;
            int n = line.length();
            while (i < n) {
                char c = line.charAt(i);
                if (c == '\'' || c == '"') {
                    int quoteEnd = findQuoteEnd(line, i, c);
                    if (quoteEnd < 0) return -1;
                    i = quoteEnd + 1;
                    // A quoted key must be followed by ':' (possibly after spaces).
                    while (i < n && line.charAt(i) == ' ') i++;
                    if (i < n && line.charAt(i) == ':') return i;
                    return -1;
                }
                if (c == '#' && i > from && (line.charAt(i - 1) == ' ' || line.charAt(i - 1) == '\t')) {
                    return -1; // comment begins before any colon
                }
                if (c == ':') {
                    if (i + 1 >= n || line.charAt(i + 1) == ' '
                            || line.charAt(i + 1) == '\t') {
                        return i;
                    }
                    // "12:30" style plain scalar (no space) keeps scanning.
                }
                if (c == '[' || c == '{') return -1; // flow collection on the key line
                i++;
            }
            return -1;
        }

        private int findQuoteEnd(String line, int start, char quote) {
            int i = start + 1;
            int n = line.length();
            while (i < n) {
                char c = line.charAt(i);
                if (quote == '\'' && c == '\'') {
                    if (i + 1 < n && line.charAt(i + 1) == '\'') {
                        i += 2;
                        continue;
                    }
                    return i;
                }
                if (quote == '"' && c == '\\') {
                    i += 2;
                    continue;
                }
                if (quote == '"' && c == '"') return i;
                i++;
            }
            return -1;
        }

        // ------------------------------------------------------------------
        // Sequences
        // ------------------------------------------------------------------

        private List<Object> parseSequence(int indent, int depth) {
            List<Object> result = new ArrayList<>();
            while (true) {
                skipInsignificant();
                if (atEnd()) break;
                int cur = indents[idx];
                if (cur != indent || !isSequenceEntry(lines[idx], cur)) break;
                String line = lines[idx];
                int contentStart = indent + 1;
                while (contentStart < line.length()
                        && (line.charAt(contentStart) == ' ' || line.charAt(contentStart) == '\t')) {
                    contentStart++;
                }
                if (contentStart >= line.length() || line.charAt(contentStart) == '#') {
                    // "- " alone: value lives on the following lines (or is null).
                    idx++;
                    Object child = parseNode(indent + 1, depth + 1);
                    result.add(child);
                    continue;
                }
                // Inline content. Rewrite the line so its indent equals the content column,
                // then recurse; nested keys of an inline map align to that same column.
                int contentIndent = contentStart;
                String content = line.substring(contentStart);
                if (content.trim().equals("---")) {
                    throw err(idx, "YAML 多文档（---）暂不支持");
                }
                lines[idx] = spaces(contentIndent) + content;
                indents[idx] = contentIndent;
                if (isSequenceEntry(lines[idx], contentIndent)) {
                    // nested sequence "- - a"
                    result.add(parseSequence(contentIndent, depth + 1));
                } else if (findMappingColon(lines[idx], contentIndent) >= 0) {
                    result.add(parseMapping(contentIndent, depth + 1));
                } else {
                    result.add(parseValueAtLine(idx, indent, depth));
                }
            }
            return result;
        }

        // ------------------------------------------------------------------
        // Mappings
        // ------------------------------------------------------------------

        private Map<String, Object> parseMapping(int indent, int depth) {
            Map<String, Object> result = new LinkedHashMap<>();
            while (true) {
                skipInsignificant();
                if (atEnd()) break;
                int cur = indents[idx];
                if (cur != indent) {
                    if (cur < indent) break;
                    throw err(idx, "YAML 缩进异常（比上一行多了 " + (cur - indent) + " 个空格）");
                }
                if (isSequenceEntry(lines[idx], cur)) break;
                String line = lines[idx];
                if (line.trim().equals("---") || line.trim().equals("...")) break;
                if (line.trim().startsWith("%")) {
                    throw err(idx, "YAML % 指令暂不支持");
                }
                if (line.charAt(indent) == '?') {
                    throw err(idx, "YAML 复杂键（? ）暂不支持");
                }
                if (line.charAt(indent) == '&' || line.charAt(indent) == '*'
                        || line.charAt(indent) == '!') {
                    throw err(idx, "YAML 锚点/别名/标签暂不支持");
                }
                int colon = findMappingColon(line, indent);
                if (colon < 0) {
                    throw err(idx, "缺少冒号：YAML 映射的每一行都需要 \"键: 值\" 结构");
                }
                String keyText = line.substring(indent, colon).trim();
                String key = parseKeyText(keyText, idx);
                String rest = line.substring(colon + 1).trim();
                if (rest.equals("---") || rest.equals("...")) {
                    throw err(idx, "YAML 多文档暂不支持");
                }
                Object value;
                if (rest.isEmpty() || rest.charAt(0) == '#') {
                    value = parseValueAfterKey(indent, depth);
                } else if (rest.startsWith("&") || rest.startsWith("*")
                        || rest.startsWith("!")) {
                    throw err(idx, "YAML 锚点/别名/标签暂不支持");
                } else if (rest.equals("|") || rest.equals("|-") || rest.equals("|+")
                        || rest.startsWith("|") && isBlockModifier(rest)
                        || rest.equals(">") || rest.equals(">-") || rest.equals(">+")
                        || rest.startsWith(">") && isBlockModifier(rest)) {
                    value = parseBlockScalar(indent, rest, keyLineIdx());
                } else {
                    value = parseValueAfterKeyInline(rest, indent, depth);
                }
                result.put(key, value);
            }
            return result;
        }

        private int keyLineIdx() {
            return idx;
        }

        private boolean isBlockModifier(String rest) {
            // | or > followed by optional digit and optional +/- (e.g. |2, >-3).
            return rest.matches("[|>][-+]?\\d?")
                    || rest.matches("[|>]\\d[-+]?");
        }

        /** Value of "key:" when nothing follows on the same line. */
        private Object parseValueAfterKey(int indent, int depth) {
            idx++;
            skipInsignificant();
            if (atEnd()) return null;
            int next = indents[idx];
            if (next > indent) {
                return parseNode(next, depth + 1);
            }
            if (next == indent && isSequenceEntry(lines[idx], next)) {
                // Sequences may sit at the same indent as their parent key.
                return parseSequence(next, depth + 1);
            }
            return null;
        }

        /** Value that starts on the key line ("key: something"). */
        private Object parseValueAfterKeyInline(String rest, int indent, int depth) {
            if (rest.startsWith("[") || rest.startsWith("{")) {
                int lineIdx = idx;
                idx++;
                return parseFlowPossiblyMultiline(rest, lineIdx, indent, depth);
            }
            if (rest.startsWith("|") || rest.startsWith(">")) {
                if (isBlockModifier(rest) || rest.matches("[|>].*")) {
                    // Only clean indicators are supported here.
                    if (isBlockModifier(rest)) {
                        return parseBlockScalar(indent, rest, keyLineIdx());
                    }
                }
            }
            if (rest.startsWith("'") || rest.startsWith("\"")) {
                int lineIdx = idx;
                idx++;
                return parseQuotedPossiblyMultiline(rest, lineIdx);
            }
            // Plain scalar: fold following more-indented lines.
            int lineIdx = idx;
            idx++;
            StringBuilder sb = new StringBuilder(stripComment(rest));
            while (!atEnd()) {
                String next = lines[idx];
                if (isSignificant(next) && indents[idx] > indent
                        && !isSequenceEntry(next, indents[idx])
                        && findMappingColon(next, indents[idx]) < 0) {
                    // Continuation of a multi-line plain scalar.
                    if (sb.length() > 0) sb.append(' ');
                    sb.append(stripComment(next.trim()));
                    idx++;
                } else if (!isSignificant(next)) {
                    // Blank/comment line inside a plain scalar: keep one blank as newline.
                    int blanks = 0;
                    while (!atEnd() && !isSignificant(lines[idx])) {
                        if (lines[idx].trim().isEmpty()) blanks++;
                        idx++;
                    }
                    if (!atEnd() && indents[idx] > indent
                            && !isSequenceEntry(lines[idx], indents[idx])
                            && findMappingColon(lines[idx], indents[idx]) < 0 && blanks > 0) {
                        sb.append('\n');
                    } else {
                        break;
                    }
                } else {
                    break;
                }
            }
            return parsePlainScalar(sb.toString(), lineIdx);
        }

        // ------------------------------------------------------------------
        // Scalars
        // ------------------------------------------------------------------

        /** Parses the value of a whole-line node (document root or sequence item). */
        private Object parseValueAtLine(int lineIdx, int indent, int depth) {
            String line = lines[lineIdx];
            String content = line.substring(indent).trim();
            if (content.equals("---")) {
                throw err(lineIdx, "YAML 多文档（---）暂不支持");
            }
            if (content.startsWith("---") && content.length() > 3
                    && (content.charAt(3) == ' ' || content.charAt(3) == '\t')) {
                throw err(lineIdx, "YAML 多文档（---）暂不支持");
            }
            if (content.startsWith("%")) {
                throw err(lineIdx, "YAML % 指令暂不支持");
            }
            if (content.startsWith("&") || content.startsWith("*")
                    || content.startsWith("!")) {
                throw err(lineIdx, "YAML 锚点/别名/标签暂不支持");
            }
            if (content.startsWith("[") || content.startsWith("{")) {
                idx = lineIdx + 1;
                return parseFlowPossiblyMultiline(content, lineIdx, indent - 1, depth);
            }
            if (content.startsWith("'") || content.startsWith("\"")) {
                idx = lineIdx + 1;
                return parseQuotedPossiblyMultiline(content, lineIdx);
            }
            if (isBlockModifier(content)) {
                idx = lineIdx + 1;
                return parseBlockScalar(indent, content, lineIdx);
            }
            idx = lineIdx + 1;
            StringBuilder sb = new StringBuilder(stripComment(content));
            while (!atEnd()) {
                String next = lines[idx];
                if (isSignificant(next) && indents[idx] > indent
                        && !isSequenceEntry(next, indents[idx])
                        && findMappingColon(next, indents[idx]) < 0) {
                    if (sb.length() > 0) sb.append(' ');
                    sb.append(stripComment(next.trim()));
                    idx++;
                } else {
                    break;
                }
            }
            return parsePlainScalar(sb.toString(), lineIdx);
        }

        private String parseKeyText(String text, int lineIdx) {
            if (text.startsWith("'") || text.startsWith("\"")) {
                Object parsed = parseSingleLineQuoted(text, lineIdx);
                return String.valueOf(parsed);
            }
            return text.trim();
        }

        private Object parseSingleLineQuoted(String text, int lineIdx) {
            char quote = text.charAt(0);
            int end = findQuoteEnd(text, 0, quote);
            if (end < 0 || end != text.length() - 1) {
                throw err(lineIdx, "YAML 引号内的键格式错误");
            }
            return quote == '\''
                    ? text.substring(1, end).replace("''", "'")
                    : unescapeDoubleQuoted(text.substring(1, end), lineIdx);
        }

        /** Single- or multi-line quoted scalar starting with rest. */
        private Object parseQuotedPossiblyMultiline(String rest, int lineIdx) {
            char quote = rest.charAt(0);
            String accumulated = rest;
            while (findQuoteEnd(accumulated, 0, quote) < 0 && !atEnd()) {
                String next = lines[idx];
                if (quote == '"' && accumulated.indexOf('\\') >= 0) {
                    // fallthrough to simple fold below
                }
                if (sbBlank(next)) {
                    accumulated += "\n";
                } else {
                    accumulated += " " + next.trim();
                }
                idx++;
            }
            int end = findQuoteEnd(accumulated, 0, quote);
            if (end < 0) {
                throw err(lineIdx, "YAML 引号未闭合");
            }
            String inner = accumulated.substring(1, end);
            // Fold newlines inside the quotes like YAML does.
            String folded = foldQuotedInner(inner);
            return quote == '\''
                    ? folded.replace("''", "'")
                    : unescapeDoubleQuoted(folded, lineIdx);
        }

        private boolean sbBlank(String line) {
            return line.trim().isEmpty();
        }

        private String foldQuotedInner(String inner) {
            return inner.replace("\n \n", "\n\n").replace("\n \n", "\n\n")
                    .replace("\n ", "\n").replace(" \n", "\n").replace('\n', ' ');
        }

        private String unescapeDoubleQuoted(String s, int lineIdx) {
            if (s.indexOf('\\') < 0) return s;
            StringBuilder sb = new StringBuilder(s.length());
            int i = 0;
            int n = s.length();
            while (i < n) {
                char c = s.charAt(i);
                if (c != '\\' || i + 1 >= n) {
                    sb.append(c);
                    i++;
                    continue;
                }
                char escape = s.charAt(++i);
                switch (escape) {
                    case 'n': sb.append('\n'); i++; break;
                    case 't': sb.append('\t'); i++; break;
                    case 'r': sb.append('\r'); i++; break;
                    case '0': sb.append('\0'); i++; break;
                    case 'a': sb.append('\u0007'); i++; break;
                    case 'b': sb.append('\b'); i++; break;
                    case 'v': sb.append('\u000B'); i++; break;
                    case 'f': sb.append('\f'); i++; break;
                    case 'e': sb.append('\u001B'); i++; break;
                    case ' ': sb.append(' '); i++; break;
                    case '"': sb.append('"'); i++; break;
                    case '/': sb.append('/'); i++; break;
                    case '\\': sb.append('\\'); i++; break;
                    case 'N': sb.append('\u0085'); i++; break;
                    case '_': sb.append('\u00A0'); i++; break;
                    case 'L': sb.append('\u2028'); i++; break;
                    case 'P': sb.append('\u2029'); i++; break;
                    case 'x':
                        if (i + 2 < n) {
                            int code = hex2(s, i + 1, 2, lineIdx);
                            sb.append((char) code);
                            i += 3;
                        } else {
                            throw err(lineIdx, "YAML \\x 转义不完整");
                        }
                        break;
                    case 'u':
                        if (i + 4 < n) {
                            int code = hex2(s, i + 1, 4, lineIdx);
                            sb.append((char) code);
                            i += 5;
                        } else {
                            throw err(lineIdx, "YAML \\u 转义不完整");
                        }
                        break;
                    case 'U':
                        if (i + 8 < n) {
                            int code = hex2(s, i + 1, 8, lineIdx);
                            sb.append(Character.toChars(code));
                            i += 9;
                        } else {
                            throw err(lineIdx, "YAML \\U 转义不完整");
                        }
                        break;
                    default:
                        throw err(lineIdx, "YAML 无效转义 \\" + escape);
                }
            }
            return sb.toString();
        }

        private int hex2(String s, int from, int count, int lineIdx) {
            int value = 0;
            for (int k = 0; k < count; k++) {
                int digit = Character.digit(s.charAt(from + k), 16);
                if (digit < 0) throw err(lineIdx, "YAML 十六进制转义含非法字符");
                value = (value << 4) | digit;
            }
            return value;
        }

        private String stripComment(String s) {
            for (int i = 0; i < s.length(); i++) {
                if (s.charAt(i) == '#' && (i == 0 || s.charAt(i - 1) == ' '
                        || s.charAt(i - 1) == '\t')) {
                    return s.substring(0, i).trim();
                }
            }
            return s.trim();
        }

        // ------------------------------------------------------------------
        // Flow collections
        // ------------------------------------------------------------------

        private Object parseFlowPossiblyMultiline(String rest, int lineIdx, int indent, int depth) {
            String accumulated = rest;
            while (!flowBalanced(accumulated) && !atEnd()) {
                accumulated += " " + lines[idx].trim();
                idx++;
            }
            if (!flowBalanced(accumulated)) {
                throw err(lineIdx, "YAML 流式集合（[]/{}）未闭合");
            }
            FlowParser flow = new FlowParser(accumulated, lineIdx, depth);
            return flow.parseValue();
        }

        private boolean flowBalanced(String s) {
            int depth = 0;
            char quote = 0;
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                if (quote != 0) {
                    if (quote == '"' && c == '\\') {
                        i++;
                        continue;
                    }
                    if (c == quote) quote = 0;
                    continue;
                }
                if (c == '\'' || c == '"') {
                    quote = c;
                } else if (c == '[' || c == '{') {
                    depth++;
                } else if (c == ']' || c == '}') {
                    depth--;
                    if (depth == 0) return true;
                }
            }
            return depth <= 0 && quote == 0;
        }

        // ------------------------------------------------------------------
        // Plain scalar typing
        // ------------------------------------------------------------------

        private Object parsePlainScalar(String text, int lineIdx) {
            String t = text.trim();
            if (t.isEmpty()) return null;
            if (t.equals("~")) return null;
            if (t.equalsIgnoreCase("null")) return null;
            if (t.equalsIgnoreCase("true")) return Boolean.TRUE;
            if (t.equalsIgnoreCase("false")) return Boolean.FALSE;
            String cleaned = t.replace("_", "");
            if (cleaned.matches("-?\\d+")) {
                try {
                    return Long.parseLong(cleaned);
                } catch (NumberFormatException tooBig) {
                    return Double.parseDouble(cleaned);
                }
            }
            if (cleaned.matches("[-+]?0x[0-9a-fA-F]+")) {
                return Long.parseLong(cleaned.substring(cleaned.indexOf('x') + 1), 16)
                        * (cleaned.startsWith("-") ? -1 : 1);
            }
            if (cleaned.matches("[-+]?0o[0-7]+")) {
                return Long.parseLong(cleaned.substring(cleaned.indexOf('o') + 1), 8)
                        * (cleaned.startsWith("-") ? -1 : 1);
            }
            if (cleaned.matches("[-+]?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?")
                    || cleaned.matches("[-+]?\\d+[eE][-+]?\\d+")) {
                return Double.parseDouble(cleaned);
            }
            if (cleaned.equals(".inf") || cleaned.equals(".Inf") || cleaned.equals(".INF")) {
                return Double.POSITIVE_INFINITY;
            }
            if (cleaned.equals("-.inf") || cleaned.equals("-.Inf") || cleaned.equals("-.INF")) {
                return Double.NEGATIVE_INFINITY;
            }
            if (cleaned.equalsIgnoreCase(".nan")) {
                return Double.NaN;
            }
            if (t.startsWith("[") || t.startsWith("{")) {
                // Plain scalar that is actually an unbalanced flow got here: surface a clear error.
                FlowParser flow = new FlowParser(t, lineIdx, 1);
                return flow.parseValue();
            }
            return t;
        }

        // ------------------------------------------------------------------
        // Block scalars
        // ------------------------------------------------------------------

        private Object parseBlockScalar(int keyIndent, String indicator, int lineIdx) {
            char style = indicator.charAt(0);
            String modifiers = indicator.substring(1);
            int chomp = 0; // 0 clip, -1 strip, 1 keep
            int explicitIndent = -1;
            for (int i = 0; i < modifiers.length(); i++) {
                char c = modifiers.charAt(i);
                if (c == '-') chomp = -1;
                else if (c == '+') chomp = 1;
                else if (c >= '1' && c <= '9') explicitIndent = c - '0';
                else throw err(lineIdx, "YAML 块标量修饰符无法识别：" + indicator);
            }
            idx = lineIdx + 1;
            int contentIndent;
            if (explicitIndent > 0) {
                contentIndent = keyIndent + explicitIndent;
                while (!atEnd() && lines[idx].trim().isEmpty()) idx++;
            } else {
                // First non-blank line decides the content indent.
                int probe = idx;
                while (probe < lines.length && lines[probe].trim().isEmpty()) probe++;
                if (probe >= lines.length) {
                    return ""; // empty block scalar
                }
                contentIndent = indents[probe];
                if (contentIndent <= keyIndent) {
                    return "";
                }
                idx = probe;
            }
            List<String> contentLines = new ArrayList<>();
            List<Integer> lineIndents = new ArrayList<>();
            while (!atEnd()) {
                String line = lines[idx];
                if (line.trim().isEmpty()) {
                    // Blank lines belong to the block but may end it (trailing).
                    contentLines.add("");
                    lineIndents.add(contentIndent);
                    idx++;
                    continue;
                }
                if (indents[idx] < contentIndent) break;
                contentLines.add(line.substring(Math.min(contentIndent, line.length())));
                lineIndents.add(indents[idx]);
                idx++;
            }
            // Remove trailing blank lines; chomping re-adds as requested.
            int lastContent = contentLines.size() - 1;
            int trailingBlanks = 0;
            while (lastContent >= 0 && contentLines.get(lastContent).isEmpty()) {
                trailingBlanks++;
                contentLines.remove(lastContent);
                lineIndents.remove(lastContent);
                lastContent--;
            }
            StringBuilder sb;
            if (style == '|') {
                sb = new StringBuilder();
                for (String line : contentLines) sb.append(line).append('\n');
            } else {
                sb = new StringBuilder();
                boolean previousBlank = false;
                boolean previousMoreIndented = false;
                for (int i = 0; i < contentLines.size(); i++) {
                    String line = contentLines.get(i);
                    if (line.isEmpty()) {
                        sb.append('\n');
                        previousBlank = true;
                        continue;
                    }
                    boolean moreIndented = lineIndents.get(i) > contentIndent
                            || line.startsWith(" ") || line.startsWith("\t");
                    if (i > 0 && !previousBlank && !moreIndented && !previousMoreIndented) {
                        sb.append(' ');
                    }
                    sb.append(line);
                    previousBlank = false;
                    previousMoreIndented = moreIndented;
                }
                if (sb.length() > 0 && sb.charAt(sb.length() - 1) != '\n') sb.append('\n');
            }
            String result = sb.toString();
            if (chomp == -1) {
                while (result.endsWith("\n")) result = result.substring(0, result.length() - 1);
            } else if (chomp == 0) {
                while (result.endsWith("\n\n")) result = result.substring(0, result.length() - 1);
            } else {
                for (int i = 0; i < trailingBlanks; i++) result += "\n";
            }
            return result;
        }

        private static String spaces(int count) {
            StringBuilder sb = new StringBuilder(count);
            for (int i = 0; i < count; i++) sb.append(' ');
            return sb.toString();
        }

        // ------------------------------------------------------------------
        // Flow parser ([..] and {..} contents)
        // ------------------------------------------------------------------

        private final class FlowParser {
            private final String s;
            private final int lineIdx;
            private int pos;
            private int depth;

            FlowParser(String s, int lineIdx, int depth) {
                // Strip a trailing comment that is outside of quotes.
                this.s = stripFlowComment(s);
                this.lineIdx = lineIdx;
                this.depth = depth;
            }

            private String stripFlowComment(String text) {
                char quote = 0;
                for (int i = 0; i < text.length(); i++) {
                    char c = text.charAt(i);
                    if (quote != 0) {
                        if (quote == '"' && c == '\\') {
                            i++;
                            continue;
                        }
                        if (c == quote) quote = 0;
                        continue;
                    }
                    if (c == '\'' || c == '"') {
                        quote = c;
                    } else if (c == '#' && i > 0
                            && (text.charAt(i - 1) == ' ' || text.charAt(i - 1) == '\t')) {
                        return text.substring(0, i);
                    }
                }
                return text;
            }

            private IllegalArgumentException err(String message) {
                return new IllegalArgumentException(
                        "YAML 第 " + (lineIdx + 1) + " 行：" + message);
            }

            Object parseValue() {
                skipWs();
                Object value = parseNode();
                skipWs();
                if (pos < s.length()) {
                    throw err("YAML 流式集合末尾有多余内容");
                }
                return value;
            }

            private void skipWs() {
                while (pos < s.length()) {
                    char c = s.charAt(pos);
                    if (c == ' ' || c == '\t' || c == '\n' || c == '\r') pos++;
                    else break;
                }
            }

            private char peek() {
                if (pos >= s.length()) throw err("YAML 流式集合意外结束");
                return s.charAt(pos);
            }

            private Object parseNode() {
                if (++depth > MAX_DEPTH) throw err("YAML 嵌套层级过深");
                try {
                    char c = peek();
                    if (c == '[') return parseFlowSequence();
                    if (c == '{') return parseFlowMapping();
                    if (c == '\'' || c == '"') return parseFlowQuoted();
                    return parseFlowPlain();
                } finally {
                    depth--;
                }
            }

            private List<Object> parseFlowSequence() {
                pos++; // '['
                List<Object> list = new ArrayList<>();
                skipWs();
                if (pos < s.length() && s.charAt(pos) == ']') {
                    pos++;
                    return list;
                }
                while (true) {
                    skipWs();
                    if (pos >= s.length()) throw err("YAML 数组未闭合");
                    if (s.charAt(pos) == ']') {
                        pos++;
                        return list;
                    }
                    list.add(parseNode());
                    skipWs();
                    if (pos >= s.length()) throw err("YAML 数组未闭合");
                    char c = s.charAt(pos);
                    if (c == ',') {
                        pos++;
                        continue;
                    }
                    if (c == ']') {
                        pos++;
                        return list;
                    }
                    throw err("YAML 数组缺少逗号");
                }
            }

            private Map<String, Object> parseFlowMapping() {
                pos++; // '{'
                Map<String, Object> map = new LinkedHashMap<>();
                skipWs();
                if (pos < s.length() && s.charAt(pos) == '}') {
                    pos++;
                    return map;
                }
                while (true) {
                    skipWs();
                    if (pos >= s.length()) throw err("YAML 对象未闭合");
                    if (s.charAt(pos) == '}') {
                        pos++;
                        return map;
                    }
                    Object key = parseNode();
                    if (!(key instanceof String)) key = String.valueOf(key);
                    skipWs();
                    if (pos >= s.length() || s.charAt(pos) != ':') {
                        throw err("YAML 对象缺少冒号");
                    }
                    pos++;
                    skipWs();
                    if (pos < s.length() && (s.charAt(pos) == ','
                            || s.charAt(pos) == '}')) {
                        map.put((String) key, null);
                    } else {
                        map.put((String) key, parseNode());
                    }
                    skipWs();
                    if (pos >= s.length()) throw err("YAML 对象未闭合");
                    char c = s.charAt(pos);
                    if (c == ',') {
                        pos++;
                        continue;
                    }
                    if (c == '}') {
                        pos++;
                        return map;
                    }
                    throw err("YAML 对象缺少逗号");
                }
            }

            private String parseFlowQuoted() {
                char quote = s.charAt(pos++);
                StringBuilder sb = new StringBuilder();
                while (true) {
                    if (pos >= s.length()) throw err("YAML 引号未闭合");
                    char c = s.charAt(pos++);
                    if (quote == '\'') {
                        if (c == '\'') {
                            if (pos < s.length() && s.charAt(pos) == '\'') {
                                sb.append('\'');
                                pos++;
                            } else {
                                return sb.toString();
                            }
                        } else {
                            sb.append(c);
                        }
                    } else {
                        if (c == '\\') {
                            if (pos >= s.length()) throw err("YAML 转义未完成");
                            char escape = s.charAt(pos++);
                            switch (escape) {
                                case 'n': sb.append('\n'); break;
                                case 't': sb.append('\t'); break;
                                case 'r': sb.append('\r'); break;
                                case '"': sb.append('"'); break;
                                case '\\': sb.append('\\'); break;
                                case '/': sb.append('/'); break;
                                case '0': sb.append('\0'); break;
                                case 'u':
                                    if (pos + 4 > s.length()) {
                                        throw err("YAML \\u 转义不完整");
                                    }
                                    int code = hex2(s, pos, 4, lineIdx);
                                    sb.append((char) code);
                                    pos += 4;
                                    break;
                                default:
                                    throw err("YAML 无效转义 \\" + escape);
                            }
                        } else if (c == '"') {
                            return sb.toString();
                        } else {
                            sb.append(c);
                        }
                    }
                }
            }

            private Object parseFlowPlain() {
                int start = pos;
                while (pos < s.length()) {
                    char c = s.charAt(pos);
                    if (c == ',' || c == ']' || c == '}' || c == '\n' || c == '\r') break;
                    // A ':' followed by a space ends a plain scalar: it separates
                    // a mapping key from its value inside flow collections.
                    if (c == ':' && (pos + 1 >= s.length() || s.charAt(pos + 1) == ' '
                            || s.charAt(pos + 1) == '\t' || s.charAt(pos + 1) == '\n'
                            || s.charAt(pos + 1) == '\r')) break;
                    pos++;
                }
                String text = s.substring(start, pos).trim();
                if (text.isEmpty()) throw err("YAML 流式集合里有空值");
                return parsePlainScalar(text, lineIdx);
            }
        }
    }
}
''',
    'app/src/main/res/drawable/ic_launcher_foreground.xml': r'''<inset xmlns:android="http://schemas.android.com/apk/res/android" android:inset="18%"><bitmap android:src="@drawable/app_icon" android:gravity="fill" android:filter="true"/></inset>''',
    'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml': r'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
''',
    'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml': r'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
''',
    'app/src/main/res/values/colors.xml': r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="launcher_background">#5757D9</color>
</resources>
''',
    'app/src/main/res/values/styles.xml': r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:statusBarColor">#F6F7FB</item>
        <item name="android:navigationBarColor">#F6F7FB</item>
        <item name="android:windowActionModeOverlay">true</item>
        <item name="android:colorAccent">#5757D9</item>
    </style>
</resources>
''',
    'app/src/test/java/com/qi/formatconverter/CoreRegressionTest.java': r'''package com.qi.formatconverter;
import org.junit.Test;
import static org.junit.Assert.*;
import java.nio.*;
import java.io.*;
import java.util.*;
import java.util.zip.*;

public class CoreRegressionTest {
    private List<TextPager.Page> pages(String text, float width) {
        return TextPager.paginate(text,s->s.codePointCount(0,s.length()),width+2,100,1,1,1,1,1,2000,1);
    }
    private List<String> lines(String text,float width){List<String> result=new ArrayList<>();for(TextPager.Page p:pages(text,width))result.addAll(p.lines);return result;}
    @Test public void chineseWrappingPreservesEveryCharacter(){String text="植物与人工智能让世界变得更有趣".repeat(100);List<String> lines=lines(text,21);assertEquals(text,String.join("",lines));for(String s:lines)assertTrue(s.codePointCount(0,s.length())<=21);}
    @Test public void supplementaryCharactersStayIntact(){String text="中🌱文𠀀".repeat(101);List<String> lines=lines(text,7);assertEquals(text,String.join("",lines));for(String s:lines){assertFalse(Character.isLowSurrogate(s.charAt(0)));assertFalse(Character.isHighSurrogate(s.charAt(s.length()-1)));assertTrue(s.codePointCount(0,s.length())<=7);}}
    @Test public void longEnglishWordWrapsWithoutLoss(){String text="A".repeat(1043);assertEquals(text,String.join("",lines(text,37)));}
    @Test public void paginationHasLimits(){try{TextPager.paginate("x\n".repeat(100),s->s.length(),10,10,1,1,1,1,1,2,1);fail();}catch(IllegalArgumentException expected){}}
    @Test public void reversePreservesStereoChannelOrder(){byte[] bytes={1,2,3,4,5,6,7,8,9,10,11,12};PcmMath.reverseStereo(bytes,12);assertArrayEquals(new byte[]{9,10,11,12,5,6,7,8,1,2,3,4},bytes);}
    @Test public void mixClipsAndFadeReachesSilence(){byte[] a=new byte[16],b=new byte[16];ByteBuffer aa=ByteBuffer.wrap(a).order(ByteOrder.LITTLE_ENDIAN),bb=ByteBuffer.wrap(b).order(ByteOrder.LITTLE_ENDIAN);for(int i=0;i<8;i++){aa.putShort((short)24000);bb.putShort((short)24000);}PcmMath.mix(a,b,16,1,1,0,4,1);aa.rewind();assertEquals(0,aa.getShort());assertEquals(0,aa.getShort());assertEquals(32767,aa.getShort());assertEquals(32767,aa.getShort());assertEquals(0,aa.getShort(12));}
    @Test public void downmixKeepsCenterSpeech() throws Exception {float[][] weights=PureJavaMp3Encoder.createDownmixWeights(6,0);ByteBuffer input=ByteBuffer.allocate(12).order(ByteOrder.LITTLE_ENDIAN);input.putShort((short)0).putShort((short)0).putShort((short)24000).putShort((short)0).putShort((short)0).putShort((short)0).flip();ByteBuffer output=PcmMath.stereo(input,2,6,weights);assertTrue(output.getShort()>5000);assertTrue(output.getShort()>5000);}
    @Test public void floatNanIsSilent(){ByteBuffer input=ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putFloat(Float.NaN);input.flip();assertEquals(0,PcmMath.sample(input,4),0);}
    @Test public void docxContainsEscapedUnicodeText() throws Exception {File f=File.createTempFile("docx-test",".docx");try{DocumentKit.write(f,24,"中文 🌱 < &\nsecond","标题",()->{});try(ZipFile zip=new ZipFile(f)){assertNotNull(zip.getEntry("[Content_Types].xml"));String xml=new String(zip.getInputStream(zip.getEntry("word/document.xml")).readAllBytes(),java.nio.charset.StandardCharsets.UTF_8);assertTrue(xml.contains("中文 🌱 &lt; &amp;"));assertTrue(xml.contains("second"));}}finally{f.delete();}}
    @Test public void epubHasUncompressedFirstMimetypeAndSpine()throws Exception{File f=File.createTempFile("epub-test",".epub");try{DocumentKit.write(f,25,"正文","标题",()->{});try(ZipInputStream z=new ZipInputStream(new FileInputStream(f))){ZipEntry first=z.getNextEntry();assertEquals("mimetype",first.getName());assertEquals(ZipEntry.STORED,first.getMethod());}try(ZipFile z=new ZipFile(f)){assertNotNull(z.getEntry("OEBPS/content.opf"));assertNotNull(z.getEntry("OEBPS/nav.xhtml"));}}finally{f.delete();}}
    @Test public void rtfUsesSignedUtf16Escapes()throws Exception{File f=File.createTempFile("rtf-test",".rtf");try{DocumentKit.write(f,28,"中🌱 {x}\\\n","标题",()->{});String text=new String(java.nio.file.Files.readAllBytes(f.toPath()),java.nio.charset.StandardCharsets.US_ASCII);assertTrue(text.contains("\\u20013?"));assertTrue(text.contains("\\u-10180?"));assertTrue(text.contains("\\{x\\}"));}finally{f.delete();}}
    @Test public void editsKeepAbsoluteTrimCoordinates(){AnimationEdits e=new AnimationEdits(2,6,1,0,0,false,false,0,100,100,Arrays.asList(new AnimationEdits.TimeRange(4,5)),Collections.emptyList());List<AnimationEdits.TimeRange> ranges=e.keptRanges(2,8);assertEquals(2,ranges.size());assertEquals(2,ranges.get(0).startSeconds,0);assertEquals(4,ranges.get(0).endSeconds,0);assertEquals(5,ranges.get(1).startSeconds,0);assertEquals(5,e.keptDurationSeconds(2,8),0);}
}
''',
    'app/src/test/java/com/qi/formatconverter/ExtraFormatsTest.java': r'''package com.qi.formatconverter;
import org.junit.Test;
import static org.junit.Assert.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Base64;

public class ExtraFormatsTest {
    private ExtraImageFormats.Raster pnm(byte[] bytes)throws Exception{return ExtraImageFormats.pnm(new PushbackInputStream(new ByteArrayInputStream(bytes),2),1000,1000,1000000);}
    @Test public void asciiPnmAcceptsFinalPixelWithoutNewline()throws Exception{
        assertArrayEquals(new int[]{0xff00ff80},pnm("P3\n# comment\n1 1\n65535\n0 65535 32768".getBytes(StandardCharsets.US_ASCII)).pixels);
    }
    @Test public void binaryPnmDoesNotEatWhitespacePixels()throws Exception{
        ByteArrayOutputStream bytes=new ByteArrayOutputStream();bytes.write("P6\r\n1 1\r\n255\r\n".getBytes(StandardCharsets.US_ASCII));bytes.write(new byte[]{32,10,35});assertEquals(0xff200a23,pnm(bytes.toByteArray()).pixels[0]);
    }
    @Test public void pbmRowPaddingIsNotAnotherPixel()throws Exception{
        ByteArrayOutputStream b=new ByteArrayOutputStream();b.write("P4\n9 2\n".getBytes(StandardCharsets.US_ASCII));b.write(new byte[]{(byte)128,(byte)128,0,0});ExtraImageFormats.Raster r=pnm(b.toByteArray());assertEquals(0xff000000,r.pixels[0]);assertEquals(0xff000000,r.pixels[8]);assertEquals(0xffffffff,r.pixels[9]);
    }
    @Test public void pamPreservesAlpha()throws Exception{
        ByteArrayOutputStream b=new ByteArrayOutputStream();b.write("P7\nWIDTH 1\nHEIGHT 1\nDEPTH 4\nMAXVAL 255\nTUPLTYPE RGB_ALPHA\nENDHDR\n".getBytes(StandardCharsets.US_ASCII));b.write(new byte[]{10,20,30,40});assertEquals(0x280a141e,pnm(b.toByteArray()).pixels[0]);
    }
    @Test public void tgaRleHonorsBottomRightOrigin()throws Exception{
        byte[] h=new byte[18];h[2]=10;h[12]=2;h[14]=2;h[16]=24;h[17]=16;ByteArrayOutputStream b=new ByteArrayOutputStream();b.write(h);b.write(1);b.write(new byte[]{0,0,(byte)255,0,(byte)255,0});b.write(0x81);b.write(new byte[]{(byte)255,0,0});ExtraImageFormats.Raster r=ExtraImageFormats.tga(new ByteArrayInputStream(b.toByteArray()),100,100,10000);assertArrayEquals(new int[]{0xff0000ff,0xff0000ff,0xff00ff00,0xffff0000},r.pixels);
    }
    @Test public void sampledRasterHasNoUnfilledCells()throws Exception{
        ExtraImageFormats.Raster r=new ExtraImageFormats.Raster(13,7,5,4,100);for(int y=0;y<7;y++)for(int x=0;x<13;x++)r.put(x,y,0xff000000|(y*13+x));for(int color:r.pixels)assertEquals(255,color>>>24);assertEquals(5,r.width);
    }
    @Test public void malformedRasterRejectedBeforeAllocation()throws Exception{
        try{new ExtraImageFormats.Raster(100000,100000,100000,100000,Long.MAX_VALUE);fail();}catch(IOException expected){}
        try{ExtraImageFormats.packBits(new byte[]{127,1},128);fail();}catch(IOException expected){}
    }
    @Test public void rtfSkipsMetadataAndDecodesUnicodeAndCodepage()throws Exception{
        String s="{\\rtf1\\ansi\\ansicpg936{\\fonttbl{\\f0 hidden;}}\\uc1\\u20013?\\u25991? \\'d6\\'d0\\'ce\\'c4\\par body}";
        assertEquals("中文 中文\nbody",ExtraTextFormats.rtfText(s));
        assertEquals("café",ExtraTextFormats.rtfText("{\\rtf1\\ansicpg1252 caf\u00e9}"));
    }
    @Test public void generatedRtfRoundTripsEmojiAndEscapes()throws Exception{
        File f=File.createTempFile("rtf-test",".rtf");try{String text="中文 🌱 {x} \\\n第二行";DocumentKit.write(f,28,text,"title",()->{});assertEquals(text,ExtraTextFormats.rtfText(new String(Files.readAllBytes(f.toPath()),StandardCharsets.ISO_8859_1)));}finally{f.delete();}
    }
    private void verifyTiff(String encoded)throws Exception{
        File f=File.createTempFile("tiff-fixture",".tiff");try{Files.write(f.toPath(),Base64.getDecoder().decode(encoded));try(RandomAccessFile input=new RandomAccessFile(f,"r")){ExtraImageFormats.Raster r=ExtraImageFormats.tiff(input,1000,1000,1000000);assertEquals(64,r.width);assertEquals(43,r.height);for(int y=0;y<43;y++)for(int x=0;x<64;x++){int color=0xff000000|(((x*17+y*23)&255)<<16)|(((x*7+y*11)&255)<<8)|((x*31+y*3)&255);assertEquals("pixel "+x+","+y,color,r.pixels[y*64+x]);}}}finally{f.delete();}
    }
@Test public void readsTiffUncompressed()throws Exception{verifyTiff("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");}
@Test public void readsTiffDeflate()throws Exception{verifyTiff("SUkqAFQgAAB4nAFAIL/fAAAAEQcfIg4+MxVdRBx8VSObZiq6dzHZiDj4mT8XqkY2u01VzFR03VuT7mKy/2nREHDwIXcPMn4uQ4VNVIxsZZOLdpqqh6HJmKjoqa8HurYmy71F3MRk7cuD/tKiD9nBIODgMef/Qu4eU/U9ZPxcdQN7hgqalxG5qBjYuR/3yiYW2y017DRU/TtzDkKSH0mxMFDQQVfvUl4OY2UtdGxMhXNrlnqKp4GpuIjIyY/n2pYG650l/KREDatjHrKCL7mhFwsDKBIiORlBSiBgWyd/bC6efTW9jjzcn0P7sEoawVE50lhY41939GaWBW21FnTUJ3vzOIISSYkxWpBQa5dvfJ6OjaWtnqzMr7PrwLoK0cEp4shI889nBNaGFd2lJuTEN+vjSPICWfkhagBAewdfjA5+nRWdrhy8vyPb0Cr64TEZ8jg4Az9XFEZ2JU2VNlS0R1vTWGLyaWkRenAwi3dPnH5urYWNvoysz5PL4Jrq8aEJAqgoE69HJLZmNb2FRsSkLhYGPx0lUCREYStjcjKCgzmhlEDApUfftk7+x1Ud2Fw86WNb+mp6C3GZHHi4LX/XPob2T40VYJQ0cZtTgqJyk6mRpLCwtbfPxr7u18UN6Mws+dNLCtpqG+GJLOioPe/HTvbmX/0FcAQkgQtDkhJioxmBtCCgxSe/1i7e5zX9+DwcCUM7GkpaK1F5PFiYTV+3XmbWb231gHQUkXszooJSs4lxxJCQ1Zev5p7O96XtCKwMGbMrKrpKO8FpTMiIXc+nRSEJVigoZy9HeDZmiT2FmkSkq0vDvFLizVkB3mAg72c/AG5eEXV9InycM4O7RIraVZH5ZpgYd583iKZWma11qrSUu7uzzMLS3cnx7tAQ/9cvEN5OIeVtMuyMQ/OrVPrKZQHpdggIhw8nmBZGqR1luiSEyyuj3DLC7Tnh/kAAD0cfIE4+MVVdQlx8U2ObZGq6dXHZhnj4l38XqIY2uY1VypR025uT7KKy/anRDrDwH7cPML4uQcVNUsxsY9OLdNqqXCwMbTMrfjpKj0FpoEiIsU+nwlbG013l5GQE9WsjBnJCF3lhKICAOYefSo6+W5XdbJz8faMbjqo6n7FZsLh4wb+X0sa2483V9NT0BdsTFuIyJ+lROPBwSfePWv6uawXNfAzsjRMLnhoqryFJwCho0S+H4jam8z3FBETkFUsDJlIiN1lBSGBgWWd/am6ee3W9jHzcnYP7rooav5E50JhY4Z938qaWA621FLTUJbvzNsISR8kxWNBQaddvet6Oi+WtczcPhD4ulUVNpkxst1OLyFqq2WHJ6mjo+28HDHYmHX1FLoRkP4uDUJKiYZnBcqDgg6f/lK4epbU9trxcx8N72Mqa6dG5+tjYC9/3HOYWLe01PvRUT/tzYAKScQmxghDQkxfvpB4OtSUtxixM1zNr6DqK+UGpCkjIG0/nLFYGPV0lTmREX2tjcHKCgXmhkoDAo4fftI7+xZUd1pw856Nb+Kp6CbGZGri4K7/XPMb2Tc0VXtQ0b9tTgOJykemRovCwikISm0kxrFBQvVdvzl6O32Wt8GzMAXPrEnoKI4EpNIhIRY9nVpaGZ52leKTEiavjmrICq7khvMBAzcdf3s5+79WdANy8EePbIur6M/EZRPg4Vf9XZgZ2dw2ViBS0mRvTqiLyuykRzDAw3TdP7j5u/0WNEEysIVPLMlrqQ2EJVGgoZW9HdnZmh32FmISkqYvDupLiy5kB3KAg7ac//q5eD7V9ILycMcO7QsraU9H5ZNgYdd83huZWl+11qPSUufuzoU0VslQ0w1tT1GJy5WmR9nCwB3fPGH7uKYUNOowsS5NLXJpqbaGJfqioj6/HoLbmsb0FwsQk08tD5NJi9dmBBuCgF+e/KO7eOfX9SvwcWwM7bApafRF5jhiYnx+3sCbWwS310jQU4zsz9EJSBUlxFlCQJ1evOF7OSWXtWmwMa3MrfHpKjYFpnoiIr4+nwJbG0Z3l4qQE86sjBLJCFblhJsCAN8efSM6+WdXdatz8e+MbjOo6nfFZrvh4v/+X0Aa2uFgYyV832mZW6211/HSUDXuzHoLSL4nxQJAQUZcvYp5Oc6VthKyMlbOrprrKt8HpyMgI2c8n6tZG+91lDOSEHeujLvLCP/nhUAAAYQcfcg4+gxVdlBx8pSObtiq6xzHZ2Dj46T8X+kY2C01VHFR0LVuTPmKyT2nRYHDwcXcPgn4uk4VNpIxstZOLxpqq16HJ6Kjo+a8HCrYmG71FLMRkPcuDTtKiX9nBcODggef/ku4eo/U9tPxcxQN71gqa5xG5z2Mb4Go68XFZAnh4E3+XJIa2NY3VRpT0V5sTaKIyealRirBwm7ePrL6uvcXNzszs39ML8NoqAeFJEuhoI++HNPamRf3FVgTkZwsDeBIiiRlBmiBgqyd/vC6ezTW93jzc70P7AEoaEVE5IlhYM193RGaWVW21ZnTUd3vziIISmYkxqpBQu5dvzJ6O3aWt7qzM/7PrELoKIcEpMshIQ89nVNaGZd2lduTEh+vjmPICqfkhugBAywdf3A5+7RWd/hy85m4e93U9CHxcGYN7KoqaO5G5TJjYXZ/3bqYWf601kLRUobtzssKSw8mx1NDQ5dfv9t4OB+UtGOxMKfNrOvqKSwGpXAjIbQ/nfhYGjx0loCREsStjwjKC0zmh5EDA9UffBk7+F1UdKFw8OWNbSmp6W3GZbHi4fX/Xjob2n40VsJQ0wZtT0qJy46mR9LCwBbfPFr7uJ8UNOMwsSdNLWtpqa+GJfOioje/Hnvbmr/0FwAQk0QtD4hJi8xmBBCCgFSe//XkhDoBAH4dfMI5+QZWdUpy8Y6PbdKr6hbEZlrg4p79XuMZ2yc2V2tS069vT/OLyDekRHvAwL/dPQP5uUQWNYgyscxPLhBrqlSEJpigoty9HyDZm2T2F6kSk+0vDDFLiHVkBLmAgP2c/UG5eYXV9cnycg4O7lIrapZH5tpgYx5832KZW6a11+rSUC7uzHMLSLcnxPtAQT9cvYN5OceVtguyMk/OrpPrKtQHpxggI1w8n6BZG+R1lCiSEGyujLDLCFIQkJYtDNpJiR5mBWKCgaae/eq7ei7X9nLwcrcM7vspaz9F54NiY8d+3AubWE+31JPQUNfszRgJSVwlxaBCQeRevih7OmyXtrCwMvTMrzjpK30Fp8EiIAU+nElbGI13lNGQERWsjVnJCZ3lheICAiYefmo6+q5XdvJz8zaMb3qo677FZALh4Eb+XIsa2M83VRNT0VdsTZuIyd+lRiPBwmfePqv6uuwXNzAzs3RML7hoq/yFJEChoIS+HMjamQz3FK48nPJZGTZ1lXqSEb6ujgLLCkbnhosAAs8cfxM4+1dVd5tx89+ObCOq6GfHZKvj4O/8XTAY2XQ1VbhR0fxuTkCKyoSnRsjDwwzcP1D4u5UVN9kxsB1OLGFqqKWHJOmjoS28HXHYmbX1FfoRkj4uDoJKisZnBwqDg06f/5K4e9bU9BrxcF8N7KMqaOdG5StjYW9/3bOYWfe01jvRUn/tzsAKSwQmx0hDQ4xfv9B4OBSUtFixMJzNrODqKSUGpWkjIQpoqU6FJZKhoda+Hhraml73FqMTkucsDytIi29lB7OBg/ed/Du6eH/W9MPzcQQP7UgoaYxE5dBhYhR93liaWpy21uDTUyTvz2kIS60kx/FBQDVdvHl6OL2WtQGzMUXPrYnoKc4EphIhIlY9nppaGt52lyKTE2avj6rIC+7khDMBAHcdfLs5+P9WdUNy8YePbcur6g/EZlPg4pf9XtgZ2xw2V2BS06RvT+iLyCykRHDAwLTdPPj5uT0WNYEyscVPLWaUtaqxMe7NrjLqKncGprsjIv8/n0NYG4d0l8uREA+tjFPKCJfmhNgDARwffWA7+aRUdehw8iyNbnCp6rTGZvji4zz/X4Eb28U0VAlQ0E1tTJGJyNWmRRnCwV3fPaH7ueYUNiowsm5NLrJpqvaGJzqio36/H8LbmAb0FEsQkI8tDNNJiRdmBVuCgZ+e/eO7eifX9mvwcqwM7vApazRF53hiY7x+3ACbWES31IjQUMzszREJSVUlxZlCQd1eviF7OcLAwgbdPkr5uo8WNtMysxdPL1trq5+EJ+OgoCe9HGvZmK/2FPASkTQvDXhLibxkBgCAgkSc/oi5eszV9xDyc1UO75kra91H5CFgYGV83KmZWO211THSUXXuzboLSf4nxkJAQoZcvsp5Ow6Vt1KyM5bOr9rrKB8HpGMgIKc8nOtZGS91lXOSEbeujfvLCj/nhoAAAsQcfwg4+0xVd5Bx89SObBiq6FzHZKDj4OT8XSkY2W01VbFR0fVuTjmKyn2nRh7szmMJSqclxutCQy9ev3N7O7eXt/uwMD/MrIPpKMQFpQgiIUw+nZBbGdR3lhiQElysjqDJCuTlhykCA20ef7E6+/VXdDlz8H2MbMGo6QXFZUnh4Y3+XdIa2hY3VlpT0p5sTuKIyyalR2rBw67eP/L6uDcXNHszsL9MLQNoqUeFJYuhoc++HhPamlf3FpgTktwsDyBIi2RlB6iBg+yd/DC6eHTW9LjzcP0P7UEoaYVE5clhYg193lGaWpW21tnTUnsY2r81VwNR00duT4uKy8+nRBPDwFfcPJv4uNwVNSAxsWROLahqqeyHJjCjonS8HrjYmvz1F0ERk4UuD8lKiA1nBFGDgJWf/Nm4eR3U9WHxcaYN7eoqai5G5nJjYrZ/3vqYWz6014LRU8btzAsKSE8mxJNDQNdfvRt4OV+UtaOxMefNrivqKmwGprAjIvQ/nzhYG3x0l8CREAStjEjKCIzmhNEDARUffVk7+Z1UdeFw8iWNbmmp6q3GZvHi4zX/XtdE5xthY19936OaW+e21CvTUG/vzLAISPQkxThBQXxdvcB6OgSWtkizMozPrtDoKxUEp1khI509n+FaGCV2lGmTEK2vjPHICTXkhXoBAb4dfgI5+kZWdopy8s6PbxKr61bEZ5rg4979XCMZ2Gc2VKtS0O9vTTOLyXekRbvAwf/dPkP5uoQWNsgyswxPL1Brq5SEJ9igoBy9HGDZmKT2FOkSkS0vDXFLibVkBfmAgj2c/oG5esXV9wnyc04O75IrazNw83eNb7up6//GZEPi4If/XMgb2Qw0VVBQ0ZRtTdiJyhymRmDCwqTfPuj7uy0UN3Ews7VNL/lpqD2GJIGioMW/HQnbmU30FZIQkdYtDhpJil5mBqKCguae/yq7e27X97Lwc/cM7DspaH9F5MNiYQd+3UubWY+31dPQUhfszlgJSpwlxuBCQyRev2h7O6yXt/CwMDTMrHjpKL0FpQEiIUU+nYlbGc13lhGQElWsjpnJCt3lhyICA2Yef6o6++5Xd4+c/9O5eBfV9FvycJwO7OAraSRH5WhgYax83fCZWjS11njSUrzuzwELS0Unx4lAQ81cvBF5OFWVtJmyMN3OrSHrKWYHpaogIe48njJZGnZ1lrqSEv6uj0LLC4bnh8sAAA8cfFM4+JdVdNtx8R+ObWOq6afHZevj4i/8XnAY2rQ1VvhR0zxuT4CKy8SnRAjDwEzcPJD4uNUVNRkxsV1OLaFqqeWHJimjom28HrHYmvX1FzoRk34uD8JKiAZnBEqDg+vJCC/lhHACALQefPg6+TxXdYBz8cSMbgio6kzFZpDh4tT+Xxka2103V6FT0+VsTCmIyG2lRLHBwPXePTn6uX4XNcIzsgZMLkpoqo6FJtKhoxa+H1ram573F+MTkCcsDGtIiK9lBPOBgTed/Xu6eb/W9gPzckQP7ogoasxE5xBhY1R935iaW9y21CDTUGTvzKkISO0kxTFBQXVdvbl6Of2WtkGzMoXPrsnoKw4Ep1IhI5Y9n9paGB52lGKTEKavjEf1FIgRkMwuDRBKiVRnBZiDgdyf/iC4emTU9qjxcu0N7zEqa3VG57ljY/1/3EGYWIW01MnRUQ3tzVIKSZYmxdpDQh5fvmJ4OqaUtuqxMy7Nr3LqK7cGp/sjID8/nINYGMd0lQuREU+tjZPKCdfmhhgDAlwffqA7+uRUdyhw82yNb7Cp6/TGZDji4Hz/XMEb2QU0VUlQ0Y1tTdGJyhWmRlnCwp3fPuH7uyYUN2ows65NL/JpqDaGJHqioL6/HQLbmKAhIOQ9nShaGWx2lbCTEfSvjjjICnzkhsEBAwUdf0k5+41Wd9Fy8BWPbFmr6J3EZOHg4SX9XWoZ2a42VfJS0jZvTnqLyr6kRwLAw0bdP4r5u88WNBMysFdPLJtrqN+EJSOgoWe9HavZme/2FjASknQvDrhLivxkB0CAg4Sc/8i5eAzV9FDycJUO7NkraR1H5WFgYaV83emZWi211nHSUrXuzvoLSz4nx4JAQ8ZcvAp5OE6VtJKyMNbOrRrrKV8HpPxNLUBpqYSGJciiogy/HlDbmpT0FtkQkx0tD2FJi6VmB+mCgC2e/HG7eLXX9PnwcT4M7YIpacZF5gpiYk5+3pKbWta31xrQU17sz6MJS+clxCtCQG9evLN7OPeXtTuwMX/MrcPpKgQFpkgiIow+ntBbGxR3l1iQE5ysj+DJCCTlhGkCAK0efPE6+TVXdXlz8b2MbgGo6kXFZonh4s3+XxIa21Y3V5pT095sTCKIyGalRKrBwO7ePTL6uXcXNbszsVh5OZyVteCyMiTOrmjrKq0HpvEgIzU8n3lZG711lAGSEEWujInLCM3nhRIAAVYcfZo4+d5VdiJx8maObqqq6u7HZzLj43b8X7sY2/81VENR0IduTMuKyQ+nRVPDwZfcPdv4uhwVNmAxsqROLuhqqyyHJ3Cjo7S8H/jYmDz1FIERkMUuDQlKiU1nBZGDgdWf/hm4el3U9qHxcuYN7yoqa25G57JjY/Z/3DqYWH601MLRUQbtzUsKSY8mxdNDQhdfvbSlRfjBwjzePoD6usUXNwkzs01ML5Foq9WFJBmhoF2+HKHamOX3FSoTkW4sDbJIifZlBjqBgn6d/sK6ewbW90rzc48P79MoaBdE5FthYJ993OOaWSe21WvTUa/vzfAISjQkxnhBQrxdvwB6O0SWt4izM8zPrBDoKFUEpJkhIN09nSFaGWV2lamTEe2vjjHICnXkhroBAv4df0I5+4ZWd8py8A6PbFKr6JbEZNrg4R79XWMZ2ac2VetS0i9vTnOLyhDRUlTtzpkKSt0mxyFDQ2Vfv6l4O+2UtDGxMHXNrLnqKP4GpUIjIYY/ncpYGg50llKREpatjtrKCx7mh2MDA6cff+s7+C9UdHNw8LeNbPup6T/GZYPi4cf/Xggb2kw0VpBQ0tRtTxiJy1ymR6DCw+TfPCj7uG0UNLEwsPVNLTlpqX2GJcGiogW/Hknbmo30FtIQkxYtD1pJi55mB+KCgCae/Gq7eK7X9PLwcTcM7Xspab9F5gNiYkd+3oubWs+31mz9XrEZ2vU2VzlS031vT8GLyAWkREnAwI3dPNH5uRYWNVoysZ5PLeJrqiaEJmqgoq69HvLZmzb2F3sSk78vDANLiEdkBIuAgM+c/RO5eVfV9ZvycdwO7iAramRH5qhgYux83zCZW3S117jSU/zuzEELSIUnxMlAQQ1cvVF5OZWVtdmyMh3OrmHrKqYHpuogIy48n3JZG7Z1l/qSED6ujILLCMbnhQsAAU8cfZM4+ddVdhtx8l+ObqOq6ufHZyvj4skpaw1F51FiY5V+39mbWB231GHQUKXszOoJSS4lxXJCQbZevfp7Oj6XtoKwMsbMrwrpK08Fp5MiI9c+nBtbGF93lKOQEOesjSvJCW/lhbACAfQefjg6+nxXdsBz8wSMb0io64zFZ9Dh4BT+XFka2J03VOFT0SVsTWmIya2lRfHBwjXePnn6ur4XNwIzs0ZML4poq86FJBKhoFa+HJramN73FSMTkWcsDatIie9lBjOBgned/ru6ev/W90Pzc4QP7yVVd2lx862Ob/Gq6DXHZHnj4L38XQIY2UY1VYpR0c5uThKKylanRprDwt7cPyL4u2cVN6sxs+9OLDNqqHeHJLujoP+8HUPYmYf1FcgRkgwuDlBKipRnBtiDgxyf/2C4e6TU9+jxcC0N7HEqaLVG5PljYT1/3YGYWcW01gnRUk3tzpIKStYmxxpDQ15fv6J4O+aUtCqxMG7NrLLqKPcGpTsjIX8/ncNYGgd0lkuREo+tjtPKCxfmh1gDA5wff+A7+4GBg8Wd/Am6eE3W9JHzcNYP7RooaV5E5aJhYeZ93iqaWm621rLTUvbvzzsIS38kx8NBQAddvEt6OI+WtNOzMRfPrVvoKZwEpeAhIiQ9nmhaGqx2lvCTEzSvj3jIC7zkhAEBAEUdfIk5+M1WdRFy8VWPbZmr6d3EZiHg4mX9XqoZ2u42VzJS03ZvT7qLy/6kRELAwIbdPMr5uQ8WNVMysZdPLdtrqh+EJmOgoqe9HuvZmy/2F3ASk7QvD/hLiDxkB92tjCHKCGXmhKoDAO4ffTI7+XZUdbpw8f6NbkKp6obGZsri4w7/X1Mb25c0V9tQ0B9tTGOJyKemROvCwS/fPXP7ubQUNfgwsjxNLoBpqsSGJwiio0y/H5Dbm9T0FBkQkF0tDKFJiOVmBSmCgW2e/bG7efXX9jnwcn4M7sIpawZF50piY45+39KbWBa31FrQUJ7szOMJSSclxWtCQa9evfN7OjeXtnuwMr/MrwPpK0QFp4giI8w+nBBbGFR3lJiQEDnZmH32FMISkQYvDUpLiY5kBdKAghac/lq5ep7V9uLycycO72sra69H5/NgYDd83HuZWL+11QPSUUfuzYgLScwnxhBAQlRcvph5OtyVtyCyM2TOr6jrK+0HpDEgIHU8nLlZGP11lUGSEYWujcnLCg3nhlIAApYcfto4+x5Vd2Jx86aOb+qq6C7HZHLj4Lb8XPsY2T81VYNR0cduTguKyk+nRpPDwtfcPxv4u1wVN6Axs+ROLChqqGyHJLCjoPS8HJYFpNoiIR4+nWJbGaZ3leqQEi6sjnLJCrblhvsCAz8ef4M6+8dXdAtz8E+MbJOo6NfFZRvh4V/+XaAa2eQ3VihT0mxsTrCIyvSlRzjBw3zeP8D6uAUXNEkzsI1MLNFoqRWFJVmhoZ2+HeHamiX3FmoTkq4sDvJIizZlB3qBg76d/AK6eEbW9IrzcM8P7RMoaVdE5ZthYd993iOaWme21qvTUu/vzzAIS3Qkx7hBQ/xdvEB6OISWtMizMQzPrVDoKPIxsTZOLXpqqb6HJgKjoka8HorYms71FxMRk1cuD5tKi99nBCODgGef/Ku4eO/U9TPxcXQN7bgqafxG5kBjYoR/3siYWwy011DRU5Ttz9kKSB0mxGFDQKVfvOl4OS2UtXGxMbXNrfnqKj4GpoIjIsY/nwpYG050l5KRE9atjBrKCF7mhKMDAOcffSs7+W9UdbNw8feNbjup6n/GZsPi4wf/X0gb24w0V9BQ0BRtTFiJyJymRODCwSTfPWj7ua0UNU5dvZJ6OdaWthqzMl7PrqLoKucEpyshI289n7NaG/d2lDuTEH+vjMPICQfkhUgBAYwdfdA5+hRWdlhy8pyPbuCr6yTEZ2jg46z9X/EZ2DU2VHlS0L1vTQGLyUWkRYnAwc3dPhH5ulYWNpoyst5PLyJrq2aEJ6qgo+69HDLZmHb2FLsSkP8vDUNLiYdkBcuAgg+c/lO5epfV9tvycxwO72Ara6RH5+hgYCx83HCZWLS11PjSUTzuzYELScUnxglAQaqJye6mRjLCwnbfPrr7uv8UN0Mws4dNL8tpqA+GJFOioJe/HNvbmR/0FWAQkaQtDehJiixmBnCCgrSe/vi7ezzX94Dwc8UM7AkpaE1F5JFiYNV+3RmbWV231aHQUeXszioJSm4lxrJCQvZevzp7O36Xt8KwMAbMrErpKI8FpNMiIRc+nVtbGZ93leOQEiesjmvJCq/lhvACAzQef3g6+7xXdABz8ESMbIio6MzFZRDh4VT+XZka2d03ViFT0mVsTga11krSUo7uztMLSxcnx1tAQ59cv+N5OCeVtGuyMK/OrPPrKTQHpXggIbw8ngBZGkR1loiSEsyujxDLC1Tnh5kAA90cfCE4+GVVdKlx8O2ObTGq6XXHZbnj4f38XkIY2oY1VspR0w5uT1KKy5anR9rDwB7cPGL4uKcVNOsxsS9OLXNqqbeHJfujoj+8HoPYmsf1FwgRk0wuD5BKi9RnBBiDgFyf/KC4eOTU9SjxcW0N7bEqafVG5jljYn1/3sGYWmLh4qb+Xusa2y83V3NT07dsT/uIyD+lRIPBwMfePQv6uUwXNZAzsdRMLhhoqlyFJqChouS+Hyjam2z3F7ETk/UsDDlIiH1lBMGBgQWd/Um6eY3W9dHzchYP7looap5E5uJhYyZ932qaW6621/LTUDbvzHsISL8kxQNBQUddvYt6Oc+WthOzMlfPrpvoKtwEpyAhI2Q9n6haG+x2lDCTEHSvjLjICPzkhUEBAYUdfck5+g1WdlFy8pWPbtmr6x3EZr8N7wMqa0dG54tjY89/3BOYWFe01JvRUN/tzSAKSWQmxahDQexfvjB4OnSUtrixMvzNr0DqK4UGp8kjIA0/nFFYGJV0lNmRER2tjWHKCaXmheoDAi4ffnI7+rZUdvpw8z6Nb4Kp68bGZAri4E7/XJMb2Nc0VRtQ0V9tTaOJyeemRivCwm/fPrP7uvQUNzgws3xNL8BpqASGJEiioIy/HNDbmRT0FVkQkZ0tDeFJiiVmBmmCgq2e/vG7ezXX93nwcxs5+19Wd6Ny8+ePbCur6G/EZLPg4Pf9XTgZ2Xw2VcBS0gRvTkiLyoykRtDAwxTdP1j5u50WN+EysCVPLGlrqK2EJPGgoTW9HXnZmb32FgISkkYvDopLis5kBxKAg1ac/5q5e97V9CLycGcO7KsraO9H5TNgYXd83buZWf+11kPSUofuzsgLSwwnx1BAQ5Rcv9h5OByVtGCyMKTOrOjrKS0HpXEgIbU8nflZGj11loGSEsWujwnLC03nh5IAA9YcfE1oeEQAKAAABAwABAAAAQAAAAAEBAwABAAAAKwAAAAIBAwADAAAA0iAAAAMBAwABAAAACAAAAAYBAwABAAAAAgAAABEBBAABAAAACAAAABUBAwABAAAAAwAAABYBAwABAAAAKwAAABcBBAABAAAASyAAABwBAwABAAAAAQAAAAAAAAAIAAgACAA=");}
@Test public void readsTiffLzw()throws Exception{verifyTiff("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");}
@Test public void readsTiffPackBits()throws Exception{verifyTiff("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");}
}
''',
    'build.gradle': r'''plugins {
    id 'com.android.application' version '9.3.1' apply false
}
''',
    'gradle.properties': r'''org.gradle.jvmargs=-Xmx3g -Dfile.encoding=UTF-8
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.configuration-cache=true
android.useAndroidX=true
android.nonTransitiveRClass=true
org.gradle.workers.max=2
''',
    'settings.gradle': r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "FormatConverter"
include(":app")
''',

    'app/src/main/java/com/qi/formatconverter/GifPlaybackPlan.java': r'''package com.qi.formatconverter;

/** A frame budget covers complete passes, never silently drops the last repeat. */
final class GifPlaybackPlan {
    static final int REVERSE_ALL = -1;
    static final int PING_PONG = -2;
    final int passes, framesPerPass, totalFrames;
    final double passSeconds, totalSeconds, actualFps;

    static int passCount(int repetitions, int reverseMode) {
        int count = Math.max(1, Math.min(100, repetitions));
        return reverseMode == PING_PONG ? count * 2 : count;
    }

    static boolean reversed(int oneBasedPass, int reverseMode) {
        return reverseMode == REVERSE_ALL
                || (reverseMode == PING_PONG && oneBasedPass % 2 == 0)
                || reverseMode == oneBasedPass;
    }

    GifPlaybackPlan(double passSeconds, int requestedFps, int frameLimit,
                    int repetitions, int reverseMode) {
        if (!Double.isFinite(passSeconds) || passSeconds <= 0)
            throw new IllegalArgumentException("剪辑后没有可用动画时长");
        passes = passCount(repetitions, reverseMode);
        if (reverseMode > passes)
            throw new IllegalArgumentException("倒放轮次不能大于内容重复次数");
        if (frameLimit < passes)
            throw new IllegalArgumentException("帧数上限不足以容纳所有循环，请增加上限或减少重复次数");
        this.passSeconds = passSeconds;
        int requested = (int) Math.min(Integer.MAX_VALUE,
                Math.ceil(passSeconds * Math.max(1, Math.min(100, requestedFps))));
        framesPerPass = Math.max(1, Math.min(requested, frameLimit / passes));
        totalFrames = framesPerPass * passes;
        totalSeconds = passSeconds * passes;
        actualFps = framesPerPass / passSeconds;
    }

    int frameIndex(int oneBasedPass, int position, int reverseMode) {
        return reversed(oneBasedPass, reverseMode) ? framesPerPass - 1 - position : position;
    }

    static int[] allocateSegments(long[] durationsUs, double speed, int fps, int limit, int passes) {
        int budget = limit / Math.max(1, passes);
        if (durationsUs.length == 0 || budget < durationsUs.length)
            throw new IllegalArgumentException("帧数上限不足以容纳所有片段和循环，请增加上限");
        long totalDuration = 0, desiredTotal = 0;
        int[] counts = new int[durationsUs.length];
        for (int i=0;i<counts.length;i++) {
            if (durationsUs[i] <= 0) throw new IllegalArgumentException("片段时长无效");
            totalDuration += durationsUs[i];
            counts[i] = (int)Math.min(Integer.MAX_VALUE, Math.max(1,
                    Math.ceil(durationsUs[i] * Math.min(100,Math.max(1,fps)) / (1e6 * speed))));
            desiredTotal += counts[i];
        }
        if (desiredTotal <= budget) return counts;
        int remaining = budget - counts.length, assigned = 0;
        double[] fractions = new double[counts.length];
        for(int i=0;i<counts.length;i++) {
            double share = remaining * (durationsUs[i] / (double)totalDuration);
            int extra = (int)Math.floor(share); counts[i] = 1 + extra;
            assigned += counts[i]; fractions[i] = share-extra;
        }
        while(assigned < budget) {
            int best = 0;
            for(int i=1;i<counts.length;i++)if(fractions[i]>fractions[best])best=i;
            counts[best]++; fractions[best] = -1; assigned++;
        }
        return counts;
    }
}
''',
    'app/src/test/java/com/qi/formatconverter/GifPlaybackTest.java': r'''package com.qi.formatconverter;

import static org.junit.Assert.*;
import org.junit.Test;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class GifPlaybackTest {
    @Test public void reverseAndPingPongKeepExactFrameOrder() {
        GifPlaybackPlan p=new GifPlaybackPlan(1,4,100,2,GifPlaybackPlan.PING_PONG);
        assertEquals(4,p.passes);assertEquals(16,p.totalFrames);
        assertEquals(0,p.frameIndex(1,0,-2));assertEquals(3,p.frameIndex(2,0,-2));
        assertEquals(0,p.frameIndex(2,3,-2));assertEquals(0,p.frameIndex(3,0,-2));
        assertTrue(GifPlaybackPlan.reversed(1,-1));assertTrue(GifPlaybackPlan.reversed(4,-1));
        assertFalse(GifPlaybackPlan.reversed(1,2));assertTrue(GifPlaybackPlan.reversed(2,2));
    }
    @Test public void frameBudgetKeepsEveryPassAndFullDuration() {
        GifPlaybackPlan p=new GifPlaybackPlan(2,30,101,3,0);
        assertEquals(3,p.passes);assertEquals(33,p.framesPerPass);assertEquals(99,p.totalFrames);
        assertEquals(6,p.totalSeconds,1e-9);assertEquals(16.5,p.actualFps,1e-9);
    }
    @Test public void maxRepeatAndTinyClipStayBounded() {
        GifPlaybackPlan p=new GifPlaybackPlan(.001,120,10000,100,-2);
        assertEquals(200,p.totalFrames);assertEquals(200,p.passes);
    }
    @Test(expected=IllegalArgumentException.class) public void impossibleBudgetExplainsFailure() {
        new GifPlaybackPlan(2,30,3,2,-2);
    }
    @Test(expected=IllegalArgumentException.class) public void invalidReversePassRejected() {
        new GifPlaybackPlan(2,30,100,1,2);
    }
    @Test public void segmentRoundingCannotDropLastRepeat() {
        int[] c=GifPlaybackPlan.allocateSegments(new long[]{210000,290000,710000},1,30,100,4);
        assertEquals(25,Arrays.stream(c).sum());for(int n:c)assertTrue(n>=1);
        assertEquals(100,Arrays.stream(c).sum()*4);
    }
    @Test(expected=IllegalArgumentException.class) public void impossibleSegmentBudgetRejected() {
        GifPlaybackPlan.allocateSegments(new long[]{100000,100000},1,30,3,2);
    }
    @Test public void playOnceOmitsNetscapeExtensionWhileInfiniteHasZero() throws Exception {
        for(int loops:new int[]{-1,0}) {
            ByteArrayOutputStream bytes=new ByteArrayOutputStream();
            try(FastGifEncoder e=new FastGifEncoder(bytes,2,2,loops,()->false)) {
                e.addIndexedFrame(new byte[]{1,2,3,4},100);e.finish();
            }
            byte[] data=bytes.toByteArray();String text=new String(data,StandardCharsets.ISO_8859_1);
            assertEquals(loops==0,text.contains("NETSCAPE2.0"));
            assertEquals(0x3b,data[data.length-1]&255);
        }
    }
    @Test public void playOncePreservesTheFinalFrameEvenWhenItMatchesTheFirst() throws Exception {
        ByteArrayOutputStream bytes=new ByteArrayOutputStream();
        try(FastGifEncoder e=new FastGifEncoder(bytes,1,1,-1,()->false)) {
            SeamlessGifWriter writer=new SeamlessGifWriter(e,100);
            writer.offer(new byte[]{0});writer.offer(new byte[]{(byte)239});writer.offer(new byte[]{0});
            writer.finishFrames(false);assertEquals(3,writer.writtenFrames());e.finish();
        }
    }
    @Test public void compressedCacheReplaysWithoutChangingPaletteIndexes() throws Exception {
        File file=File.createTempFile("gif-loop-test",".cache");
        try(IndexedFrameStore store=new IndexedFrameStore(file,4,()->false)) {
            store.add(new byte[]{1,2,3,4});store.add(new byte[]{9,8,7,6});
            byte[] out=new byte[4];store.read(1,out);assertArrayEquals(new byte[]{9,8,7,6},out);
            store.read(0,out);assertArrayEquals(new byte[]{1,2,3,4},out);
        }
        assertFalse(file.exists());
    }
}
''',
    'app/src/androidTest/java/com/qi/formatconverter/GifExportDeviceTest.java': r'''package com.qi.formatconverter;

import android.app.Instrumentation;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.view.View;
import android.widget.Spinner;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;
import java.io.*;
import java.lang.reflect.*;
import java.util.*;
import org.junit.Test;
import org.junit.runner.RunWith;
import pl.droidsonroids.gif.GifDrawable;
import static org.junit.Assert.*;

@RunWith(AndroidJUnit4.class)
public class GifExportDeviceTest {
    private static Object get(Object target,String name)throws Exception {
        Field f=target.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(target);
    }
    @Test public void gifControlsRecommendationAndReverseExportWorkTogether() throws Exception {
        Instrumentation instrumentation=InstrumentationRegistry.getInstrumentation();
        Context context=instrumentation.getTargetContext();
        File input=File.createTempFile("gif-input-",".gif",context.getCacheDir()),output=null;
        try(OutputStream out=new FileOutputStream(input);FastGifEncoder e=new FastGifEncoder(out,8,6,0,()->false)) {
            int[] colors=new int[48];byte[] indexes=new byte[48];
            for(int color:new int[]{0xffff0000,0xff00ff00,0xff0000ff}) {
                Arrays.fill(colors,color);e.addFrame(colors,indexes,100);
            }
            e.finish();
        }
        MainActivity activity=(MainActivity)instrumentation.startActivitySync(
                new Intent(context,MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
        try {
            Throwable[] failure={null};
            instrumentation.runOnMainSync(()->{try {
                Class<?> format=Class.forName(MainActivity.class.getName()+"$SourceFormat");
                Object gif=Enum.valueOf((Class)format,"GIF");
                Class<?> item=Class.forName(MainActivity.class.getName()+"$SelectedItem");
                Constructor<?> ctor=item.getDeclaredConstructor(Uri.class,String.class,String.class,long.class,format);
                ctor.setAccessible(true);
                ((List)get(activity,"selectedItems")).add(ctor.newInstance(Uri.fromFile(input),"test.gif","image/gif",input.length(),gif));
                Method selection=MainActivity.class.getDeclaredMethod("updateSelectionUi");selection.setAccessible(true);selection.invoke(activity);
                int gifPosition=((List)get(activity,"visibleOutputFormats")).indexOf(3);
                assertTrue(gifPosition>=0);((Spinner)get(activity,"formatSpinner")).setSelection(gifPosition);
                ((Spinner)get(activity,"resolutionSpinner")).setSelection(1);
                Field edits=MainActivity.class.getDeclaredField("animationEdits");edits.setAccessible(true);edits.set(activity,AnimationEdits.NONE);
                Method refresh=MainActivity.class.getDeclaredMethod("updateControlStates");refresh.setAccessible(true);refresh.invoke(activity);
                for(String name:new String[]{"videoLoopSpinner","reverseLoopSpinner","gifReplaySpinner","recommendationText"}) {
                    assertEquals(name,View.VISIBLE,((View)get(activity,name)).getVisibility());
                }
            }catch(Throwable e){failure[0]=e;}});
            if(failure[0]!=null)throw new AssertionError(failure[0]);
            Method export=MainActivity.class.getDeclaredMethod("gifToGif",Uri.class,String.class,int.class,int.class,int.class,int.class);
            export.setAccessible(true);Object result=export.invoke(activity,Uri.fromFile(input),"test.gif",10,100,1,GifPlaybackPlan.REVERSE_ALL);
            output=(File)get(result,"file");assertTrue(output.length()>0);
            GifDrawable decoded=new GifDrawable(output);
            try {
                decoded.stop();assertEquals(3,decoded.getNumberOfFrames());
                int[] dominantChannels={0,8,16};
                for(int i=0;i<3;i++) {
                    Bitmap frame=decoded.seekToFrameAndGet(i);
                    try {
                        int color=frame.getPixel(3,2);int channel=(color>>>dominantChannels[i])&255;
                        assertTrue("frame "+i,channel>180);
                        for(int shift:new int[]{0,8,16})if(shift!=dominantChannels[i])assertTrue(((color>>>shift)&255)<80);
                    } finally {frame.recycle();}
                }
            } finally {decoded.recycle();}
        } finally {
            instrumentation.runOnMainSync(activity::finish);input.delete();if(output!=null)output.delete();
        }
    }
}
''',
}

def generate_icons(output, source):
    from PIL import Image, ImageOps
    image = Image.open(source).convert("RGBA")
    resources = output / "app/src/main/res"
    for density, side in (("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)):
        directory = resources / ("mipmap-" + density)
        directory.mkdir(parents=True, exist_ok=True)
        icon = Image.new("RGBA", (side,side), (70,73,230,255))
        thumb = ImageOps.contain(image, (side,side), Image.Resampling.LANCZOS)
        icon.alpha_composite(thumb, ((side-thumb.width)//2,(side-thumb.height)//2))
        for name in ("ic_launcher.png","ic_launcher_round.png"):
            icon.save(directory / name)
    directory = resources / "drawable-nodpi"
    directory.mkdir(parents=True, exist_ok=True)
    ImageOps.contain(image,(432,432),Image.Resampling.LANCZOS).save(directory / "app_icon.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=".", help="Generated Android project directory")
    parser.add_argument("--icon", help="Override the repository root app icon")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    icon = Path(args.icon) if args.icon else Path(__file__).resolve().parent / "转换.png"
    if not icon.is_file():
        raise SystemExit("App icon is missing: " + str(icon))
    for name, content in SOURCES.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    generate_icons(output, icon)
    print(f"Generated {len(SOURCES)} source/resource files and launcher icons in {output}")

if __name__ == "__main__":
    main()
