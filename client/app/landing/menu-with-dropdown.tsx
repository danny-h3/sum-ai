'use client'

import { Menu } from "@mantine/core"
import { IconUpload } from "@tabler/icons-react"
import React, {useRef} from "react";

export function MenuDropDown(props: {button: React.ReactNode, onFileSelect: (files: File[]) => void}) {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    }
    
    return (
        <>
            <Menu width={200} position="bottom-start">
                <Menu.Target>
                    {props.button}
                </Menu.Target>

                <Menu.Dropdown>
                    <Menu.Item leftSection={<IconUpload size={14}/>} onClick={handleUploadClick}> Upload File </Menu.Item>
                </Menu.Dropdown>
            </Menu>

            <input 
                type="file" 
                ref={fileInputRef} 
                style={{display: 'none'}} 
                onChange={ (e) => props.onFileSelect(Array.from(e.target.files ?? []))}
            />
        </>
    )
}