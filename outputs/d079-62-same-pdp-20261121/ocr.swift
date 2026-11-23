// 그림 속 글자를 읽어 한 줄씩 출력한다(macOS 내장 글자 인식). 사용: swift ocr.swift 그림1 그림2 ...
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("##FILE\t\(path)\tERROR"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.recognitionLanguages = ["en-US", "es-ES", "fr-FR"]
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let lines = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }
    print("##FILE\t\(path)\t" + lines.joined(separator: " ¦ "))
}
