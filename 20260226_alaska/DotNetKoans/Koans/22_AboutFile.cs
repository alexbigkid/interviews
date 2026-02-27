using System;
using System.Collections.Generic;
using Xunit;
using System.IO;
using System.Text;
using DotNetKoans.Engine;
using IOPath = System.IO.Path;

namespace DotNetKoans.Koans;

public class AboutFile : Koan, IDisposable
{
	private readonly List<string> _filesToCleanup = new List<string>();

	public void Dispose()
	{
		foreach (var file in _filesToCleanup)
		{
			if (File.Exists(file))
				File.Delete(file);
		}
	}

	private string TrackFile(string path)
	{
		_filesToCleanup.Add(path);
		return path;
	}
	// File is a class that provides static methods for creating, copying, deleting, moving,
	// and opening files, and helps in the creation of FileStream objects.

	[Step(1)]
	public void CreatingAndDeletingFile()
	{
		string path = TrackFile(IOPath.GetTempFileName()); // GetTempFileName() Creates a uniquely named, zero-byte temporary file on disk and returns the full path of that file.
		Assert.Equal(true, File.Exists(path));
		File.Delete(path);
		Assert.Equal(false, File.Exists(path));
	}

	[Step(2)]
	public void CopyFile()
	{
		string path = TrackFile(IOPath.GetTempFileName());
		string newPath = TrackFile(IOPath.Combine(IOPath.GetTempPath(), "newFile.txt"));

		File.Delete(newPath);
		File.Copy(path, newPath);

		Assert.Equal(true, File.Exists(path));
		Assert.Equal(true, File.Exists(newPath));
	}

	[Step(3)]
	public void MoveFile()
	{
		string path = TrackFile(IOPath.GetTempFileName());
		string newPath = TrackFile(IOPath.Combine(IOPath.GetTempPath(), "newFile.txt"));

		File.Delete(newPath);
		File.Move(path, newPath);

		Assert.Equal(false, File.Exists(path));
		Assert.Equal(true, File.Exists(newPath));
	}

	[Step(4)]
	public void GetFileInfo()
	{
        // string fixedFileName= "fixedFileName.txt";
		string path = TrackFile(IOPath.GetTempFileName());
		FileInfo fileInfo = new FileInfo(path);

		Assert.Equal(true, fileInfo.Exists);
		Assert.Equal(path, fileInfo.FullName); // what is the file name?
	}

	[Step(5)]
	public void ReadFile()
	{
		string data = "Hello World!";
		string path = createFileAndFillIn(data);

		byte[] bytes = new byte[data.Length];
		UTF8Encoding temp = new UTF8Encoding(true);
		string readMessage = "";
		using (FileStream fs = File.OpenRead(path))
		{
			while (fs.Read(bytes, 0, bytes.Length) > 0)
			{
				readMessage = temp.GetString(bytes);
			}
		}
		Assert.Equal(data, readMessage); // what is the message?
	}

	[Step(6)]
	public void ReadLines()
	{

		string data = "Line0\nLine1\nLine2";
		string path = createFileAndFillIn(data);

		var lines = File.ReadAllLines(path);

		Assert.Equal(3, lines.Length); // what is the number of lines?
		Assert.Equal("Line1", lines[1]); // what is written in the line No.2 ?
	}

	private string createFileAndFillIn(string data)
	{
		string path = TrackFile(IOPath.GetTempFileName());
		byte[] info = new UTF8Encoding(true).GetBytes(data);
		using (FileStream fs = File.OpenWrite(path))
		{
			fs.Write(info, 0, info.Length);
		}
		return path;
	}
}
