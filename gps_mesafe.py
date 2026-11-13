#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gps_mesafe.py
İki GPS koordinatı arasındaki mesafeyi Haversine formülü kullanarak
metre ve kilometre cinsinden hesaplayan program.
"""

import math
import sys
from typing import Tuple

# Dünya'nın ortalama yarıçapı (metre cinsinden)
DUNYA_YARICAPI_METRE = 6371000.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
    """
    İki GPS koordinatı (enlem, boylam) arasındaki mesafeyi Haversine formülü ile hesaplar.

    Parametreler:
        lat1 (float): 1. noktanın enlemi (derece)
        lon1 (float): 1. noktanın boylamı (derece)
        lat2 (float): 2. noktanın enlemi (derece)
        lon2 (float): 2. noktanın boylamı (derece)

    Döndürür:
        Tuple[float, float]: (mesafe_metre, mesafe_kilometre)
    """
    # Dereceleri radyana dönüştür
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formülü
    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )

    # Sayısal yuvarlama hatalarından kaçınmak için a'yı [0, 1] aralığında sınırla
    a = min(1.0, max(0.0, a))

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    mesafe_m = DUNYA_YARICAPI_METRE * c
    mesafe_km = mesafe_m / 1000.0

    return mesafe_m, mesafe_km


def gecerli_koordinat_mi(lat: float, lon: float) -> bool:
    """Enlem ve boylam değerlerinin coğrafi sınırlar içinde olup olmadığını doğrular."""
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0


def float_girdisi_al(istek_metni: str, min_val: float, max_val: float) -> float:
    """Kullanıcıdan geçerli aralıkta bir float değeri alır."""
    while True:
        try:
            giris = input(istek_metni).strip().replace(",", ".")
            deger = float(giris)
            if min_val <= deger <= max_val:
                return deger
            print(f"Hata: Değer {min_val} ile {max_val} arasında olmalıdır. Tekrar deneyin.")
        except ValueError:
            print("Hata: Geçerli bir sayısal değer giriniz (örnek: 41.0082).")
        except (KeyboardInterrupt, EOFError):
            print("\nİşlem kullanıcı tarafından iptal edildi.")
            sys.exit(0)


def kullanicidan_koordinat_al(nokta_adi: str) -> Tuple[float, float]:
    """Belirtilen nokta için enlem ve boylam girdilerini alır."""
    print(f"\n--- {nokta_adi} Koordinatları ---")
    lat = float_girdisi_al(f"{nokta_adi} Enlem [-90, +90]: ", -90.0, 90.0)
    lon = float_girdisi_al(f"{nokta_adi} Boylam [-180, +180]: ", -180.0, 180.0)
    return lat, lon


def main():
    print("=" * 55)
    print("      GPS Mesafe Hesaplayıcı (Haversine Formülü)      ")
    print("=" * 55)

    lat1, lon1 = kullanicidan_koordinat_al("1. Nokta")
    lat2, lon2 = kullanicidan_koordinat_al("2. Nokta")

    mesafe_m, mesafe_km = haversine(lat1, lon1, lat2, lon2)

    print("\n" + "=" * 55)
    print("                   HESAPLAMA SONUCU                  ")
    print("=" * 55)
    print(f"1. Nokta       : Enlem {lat1:10.6f}°, Boylam {lon1:10.6f}°")
    print(f"2. Nokta       : Enlem {lat2:10.6f}°, Boylam {lon2:10.6f}°")
    print("-" * 55)
    print(f"Mesafe (Metre) : {mesafe_m:,.2f} m")
    print(f"Mesafe (Km)    : {mesafe_km:,.4f} km")
    print("=" * 55)


if __name__ == "__main__":
    main()
