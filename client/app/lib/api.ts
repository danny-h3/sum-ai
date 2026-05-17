import { FileWithPath } from "@mantine/dropzone"

// Make call to /upload/ fast api endpooint, requires data + files
export async function PostUpload(userInput: string, files: FileWithPath[]) {
    // hard code endpoint for now, add env functionality later
    const endpoint = "http://localhost:8080/upload/"

    if ( (!userInput) && (files.length === 0)) {
        console.error("Input fields can't be empty")
        return
    }

    try{ 
        // construct form for endpoint
        const formData = new FormData();
        formData.append("input", userInput); 
        for ( const file of files ) {
            formData.append("files", file)
        }

        // try to send to backend
        const response = await fetch(endpoint, {
            method: 'POST', 
            body: formData
        })
        
        return response.status
    } catch (err) { 
        return err
    }
}