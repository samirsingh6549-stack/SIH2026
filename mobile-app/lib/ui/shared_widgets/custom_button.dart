import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final IconData? icon;
  final VoidCallback? onPressed;
  final Color backgroundColor;
  final Color textColor;
  final bool isLoading;
  final double height;

  const CustomButton({
    super.key,
    required this.text,
    this.icon,
    required this.onPressed,
    this.backgroundColor = AppColors.primary,
    this.textColor = const Color(0xFF0F172A),
    this.isLoading = false,
    this.height = 48.0,
  });

  factory CustomButton.danger({
    required String text,
    IconData? icon,
    required VoidCallback? onPressed,
    bool isLoading = false,
  }) {
    return CustomButton(
      text: text,
      icon: icon,
      onPressed: onPressed,
      backgroundColor: AppColors.criticalRed,
      textColor: Colors.white,
      isLoading: isLoading,
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height,
      width: double.infinity,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
          foregroundColor: textColor,
          disabledBackgroundColor: backgroundColor.withOpacity(0.5),
        ),
        child: isLoading
            ? SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(strokeWidth: 2, color: textColor),
              )
            : Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (icon != null) ...[
                    Icon(icon, size: 18, color: textColor),
                    const SizedBox(width: 8),
                  ],
                  Text(
                    text,
                    style: TextStyle(
                      color: textColor,
                      fontSize: 14,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 0.5,
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}
