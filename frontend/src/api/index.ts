import axios from "axios";

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    await axios.post(`${import.meta.env.VITE_API_BASE_URL}/file/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: true,
    });
}


