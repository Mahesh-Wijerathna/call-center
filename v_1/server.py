import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc.contrib.media import MediaPlayer, MediaBlackhole

async def run(pc, signaling):
    await signaling.connect()

    @pc.on("track")
    def on_track(track):
        if track.kind == "audio":
            print("Receiving audio track")
            player = MediaPlayer(track)
            player.play()

    # Wait for an offer from the signaling server
    await signaling._connect()
    description = await signaling.receive()
    await pc.setRemoteDescription(description)
    await pc.setLocalDescription(await pc.createAnswer())
    await signaling.send(pc.localDescription)

    # Wait for the connection to close
    await pc.close()

if __name__ == "__main__":
    pc = RTCPeerConnection()
    # Change the IP and port to match the signaling server setup
    signaling = TcpSocketSignaling("192.168.1.118", 8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(pc, signaling))
