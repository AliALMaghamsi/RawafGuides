import React, { useState } from 'react'
import api from '../api/api'




const UploadFile = ({uploadUrl , inputId}) => {
  const [selectedFile , setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [error , setError] = useState('');

  const onFileChange = (event) => {
    const file =event.target.files[0];

    if (file){
      const allowedFormats = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        
      ]
      const allowedExtensions = [".xlsx" ,".xls"];
      
      const fileExtension = file.name.substring(file.name.lastIndexOf("."))
      if (allowedFormats.includes(file.type) && allowedExtensions.includes(fileExtension.toLowerCase())){
        setError("");
        setSelectedFile(file);
      } else {
        setSelectedFile(null);
        setError("invalid file type: please select an Excel ('.xlsx' 'xls') file ");
      }
    }
    
  };

  const onFileUpload = async() => {
    if (!selectedFile){
      setError("please select file first");
      return;
    }
    const formdata = new FormData();
    formdata.append("file",selectedFile,selectedFile.name)

    try {
      const response = await api.post(uploadUrl ,formdata , {
        headers: {'Content-Type': 'multipart/form-data'},
      }) ;
      
      const result = response.data;
      setUploadResult(result);
      
      setSelectedFile(null);
      setError("");


    } catch(error){
      console.log(error);
      alert("file uploaded field.");

    }

  }
  return (
    <>
        <div className="w-full max-w-md mt-5 ml-10">
            
            
            {/* Input and button in one horizontal row */}
            <div className="flex items-center gap-3">
                <label
                htmlFor={inputId}
                className="flex items-center justify-center w-full h-11 px-4 text-sm text-gray-700 bg-gray-100 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-200 transition-colors"
                >
                {selectedFile ? selectedFile.name : "Choose file"}
                <input
                    id={inputId}
                    type="file"
                    onChange={onFileChange}
                    accept=".xlsx, .xls, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                    className="hidden"
                />
                </label>

                <button
                onClick={onFileUpload}
                disabled={!selectedFile}
                className={`h-11 px-6 rounded-lg text-white font-medium transition-colors ${
                    selectedFile
                    ? 'bg-black hover:bg-gray-800'
                    : 'bg-gray-500 cursor-not-allowed'
                }`}
                >
                Upload
                </button>
            </div>

            {/* Error message */}
            {error && <p className="text-red-600 mt-2">{error}</p>}

            {/* Upload result */}
            {uploadResult && (
                <div className="mt-4 border p-3 rounded bg-gray-100">
                  <h2 className="font-semibold text-lg text-green-700">Upload Summary</h2>
                  <p>✅ Inserted: {uploadResult.Inserted}</p>
                  <p>⚠️ warnings: {uploadResult.Warnings.length}</p>
                  <p>❌ Failed: {uploadResult.Failed}</p>

                  {uploadResult.Errors && uploadResult.Errors.length > 0 && (
                      <div className="mt-2">
                      <h3 className="font-medium text-red-600">Error Details:</h3>
                      <ul className="list-disc list-inside text-red-500">
                          {uploadResult.Errors.map((err, index) => (
                          <li key={index}>{err}</li>
                          ))}
                      </ul>
                      </div>
                  )}
                  {uploadResult.Warnings && uploadResult.Warnings.length > 0 && (
                      <div className="mt-2">
                      <h3 className="font-medium text-orange-400">Warnings Details:</h3>
                      <ul className="list-disc list-inside text-orange-400">
                          {uploadResult.Warnings.map((warr, index) => (
                          <li key={index}>{warr}</li>
                          ))}
                      </ul>
                      </div>
                  )}
                </div>
            )}
        </div>


     
    </>
    
  )
}

export default UploadFile






{/* <div className="relative flex w-full max-w-[24rem] mt-5 mx-4">
        

      <label className="whitespace-nowrap  px-3 mb-2 text-sm font-medium text-white bg-gray-400 dark:text-white rounded-lg mr-3" htmlFor="file_input">Upload file</label>
      <input className="mr-3 w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" id="file_input" type="file" onChange={onFileChange}
      accept=".xlsx, .xls, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"/>

      {error && <p className='text-red-600'>{error}</p>}
      

      <button onClick={onFileUpload} disabled={!selectedFile} 
      className={`px-4 py-2 rounded-lg text-white font-medium transition-colors ${
        selectedFile
        ? 'bg-black hover:bg-gray-800'
        : 'bg-gray-500 cursor-not-allowed'
        }`}
      > Upload

      </button>
            {uploadResult && (
                <div className="mt-4 border p-3 rounded bg-gray-100">
                    <h2 className="font-semibold text-lg text-green-700">Upload Summary</h2>
                    <p>✅ Inserted: {uploadResult.Inserted}</p>
                    <p>❌ Failed: {uploadResult.Failed}</p>

                    {uploadResult.Errors && uploadResult.Errors.length > 0 && (
                    <div className="mt-2">
                        <h3 className="font-medium text-red-600">Error Details:</h3>
                        <ul className="list-disc list-inside text-red-500">
                        {uploadResult.Errors.map((err, index) => (
                            <li key={index}>{err}</li>
                        ))}
                        </ul>
                    </div>
                    )}
                </div>
            )}

    </div> */}