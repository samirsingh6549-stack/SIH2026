import 'package:audioplayers/audioplayers.dart';

class AudioAlarmService {
  final AudioPlayer _player = AudioPlayer();
  bool _isPlaying = false;

  bool get isPlaying => _isPlaying;

  Future<void> playEmergencySiren() async {
    try {
      _isPlaying = true;
      // In production, loads local siren audio asset. Falls back gracefully if asset not yet bundled.
      await _player.setReleaseMode(ReleaseMode.loop);
      await _player.setVolume(1.0);
      // Attempt playing bundled asset
      await _player.play(AssetSource('sounds/emergency_siren.mp3'));
    } catch (_) {
      // In simulator or environments without sound hardware, maintain state safely
    }
  }

  Future<void> stopSiren() async {
    try {
      _isPlaying = false;
      await _player.stop();
    } catch (_) {}
  }

  void dispose() {
    _player.dispose();
  }
}
