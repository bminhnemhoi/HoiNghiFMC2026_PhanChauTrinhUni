# Cài gói R cho phân tích xác nhận (T6.0) vào thư viện của người dùng — không cần quyền quản trị.
#   Rscript analysis_R/setup.R
pkgs <- c("lme4", "glmmTMB", "sandwich", "boot", "jsonlite", "arrow")
lib <- Sys.getenv("R_LIBS_USER")
if (!nzchar(lib)) lib <- file.path(Sys.getenv("LOCALAPPDATA"), "R", "win-library",
                                   paste(R.version$major, strsplit(R.version$minor, ".", fixed = TRUE)[[1]][1], sep = "."))
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
need <- pkgs[!vapply(pkgs, requireNamespace, logical(1), quietly = TRUE)]
if (length(need)) install.packages(need, lib = lib, repos = "https://cloud.r-project.org", type = "binary")
ok <- vapply(pkgs, requireNamespace, logical(1), quietly = TRUE)
print(data.frame(package = pkgs, installed = ok))
cat("R", R.version.string, "| lib:", lib, "\n")
if (!all(ok)) quit(status = 1)
