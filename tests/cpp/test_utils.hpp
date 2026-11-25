#pragma once

#include <filesystem>
#include <fstream>                          
#include <random>
#include <string>

namespace fs = std::filesystem;
// Fichier temporaire unique, supprime automatiquement a la destruction
struct TmpFile
{
    fs::path path;

    explicit TmpFile(const std::string& content)
    {
        path = fs::temp_directory_path()
             / ("mlp_test_" + std::to_string(std::random_device{}()) + ".csv");
        std::ofstream(path) << content;
    }
    ~TmpFile() { fs::remove(path); }

    TmpFile(const TmpFile&) = delete;
    TmpFile& operator=(const TmpFile&) = delete;
};