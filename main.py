import discord
client = discord.Bot(intents=discord.Intents.all())

@client.command(description="通話の録音を開始します")
async def start_record(ctx:discord.ApplicationContext):
    try:
        vChannel = await ctx.author.voice.channel.connect()
        await ctx.respond("録音を開始します。")
    except AttributeError:
        await ctx.respond("ボイスチャンネルに参加した状態でコマンドを実行してください。")
        return
    
    ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)

async def finished_callback(sink:discord.sinks.MP3Sink, ctx:discord.ApplicationContext):
    recordedUsers = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]

    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await ctx.channel.send(f"録音を終了しました。音声ファイルを送信しました。{', '.join(recordedUsers)}.", files=files)

@client.command(description="通話の録音を終了します")
async def stop_record(ctx:discord.ApplicationContext):
    ctx.voice_client.stop_recording()
    await ctx.respond("録音を終了します。")
    await ctx.voice_client.disconnect()

client.run("YOUR_TOKEN_HERE")